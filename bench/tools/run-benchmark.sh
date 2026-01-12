#!/usr/bin/env bash
# Run token efficiency benchmarks with incremental persistence
#
# Usage:
#   ./run-benchmark.sh                           # Show help
#   ./run-benchmark.sh --list                    # List all tests
#   ./run-benchmark.sh --list-remaining          # List tests not yet run
#   ./run-benchmark.sh --all                     # Run ALL tests (careful!)
#   ./run-benchmark.sh --format stele-ascii      # Run all tests for one format
#   ./run-benchmark.sh --model sonnet            # Run all tests for one model
#   ./run-benchmark.sh --dataset flat/100        # Run all tests for one dataset
#   ./run-benchmark.sh --format stele-ascii --model sonnet --dataset flat/100  # Single test
#   ./run-benchmark.sh --batch 10                # Run next 10 untested combinations

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
BENCH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENCODED_DIR="$BENCH_DIR/encoded"
PROMPTS_DIR="$BENCH_DIR/prompts"
RESULTS_DIR="$BENCH_DIR/results"
TOOLS_DIR="$BENCH_DIR/tools"
SESSIONS_DIR="$BENCH_DIR/sessions"

RESULTS_FILE="$RESULTS_DIR/token-counts.jsonl"
LOG_FILE="$RESULTS_DIR/benchmark.log"

# Test parameters
FORMATS=("json" "stele-ascii" "stele-light" "stele-full" "toon")
MODELS=("opus" "sonnet" "haiku")
DATASETS=("flat/10" "flat/50" "flat/100" "flat/500" "nested/shallow" "nested/medium" "nested/deep")

# Model name mapping for claude CLI
declare -A MODEL_NAMES=(
    ["opus"]="claude-opus-4-5-20251101"
    ["sonnet"]="claude-sonnet-4-5-20250929"
    ["haiku"]="claude-3-5-haiku-20241022"
)

# Initialize results file if it doesn't exist
mkdir -p "$RESULTS_DIR"
touch "$RESULTS_FILE"

# === CLAUDE.md HANDLING ===
# We want raw Claude without Q's identity for accurate benchmarks
CLAUDE_MD="$HOME/.claude/CLAUDE.md"
CLAUDE_MD_BACKUP="$HOME/.crewu/tmp/CLAUDE.md.benchmark-backup"

backup_claude_md() {
    if [[ -f "$CLAUDE_MD" ]]; then
        echo -e "${YELLOW}[benchmark] Backing up CLAUDE.md to get raw Claude...${NC}"
        mkdir -p "$(dirname "$CLAUDE_MD_BACKUP")"
        cp "$CLAUDE_MD" "$CLAUDE_MD_BACKUP"
        rm "$CLAUDE_MD"
        echo -e "${GREEN}[benchmark] CLAUDE.md removed for clean benchmark${NC}"
    fi
}

restore_claude_md() {
    if [[ -f "$CLAUDE_MD_BACKUP" ]]; then
        echo -e "${YELLOW}[benchmark] Restoring CLAUDE.md...${NC}"
        mv "$CLAUDE_MD_BACKUP" "$CLAUDE_MD"
        echo -e "${GREEN}[benchmark] CLAUDE.md restored${NC}"
    fi
}

# Trap to ensure restore happens even on script exit/interrupt
trap restore_claude_md EXIT INT TERM

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# Check if a test has been completed
test_completed() {
    local format="$1"
    local model="$2"
    local dataset="$3"

    if [[ ! -f "$RESULTS_FILE" ]]; then
        return 1
    fi

    grep -q "\"format\":\"$format\".*\"model\":\"$model\".*\"dataset\":\"$dataset\"" "$RESULTS_FILE" && return 0 || return 1
}

# Generate all test combinations
generate_all_tests() {
    for format in "${FORMATS[@]}"; do
        for model in "${MODELS[@]}"; do
            for dataset in "${DATASETS[@]}"; do
                echo "$format $model $dataset"
            done
        done
    done
}

# List all tests
list_all() {
    echo -e "${BLUE}All test combinations:${NC}"
    local count=0
    generate_all_tests | while read -r format model dataset; do
        count=$((count + 1))
        printf "%3d. format=%-12s model=%-6s dataset=%s\n" "$count" "$format" "$model" "$dataset"
    done
}

# List remaining tests
list_remaining() {
    echo -e "${BLUE}Remaining test combinations:${NC}"
    local count=0
    generate_all_tests | while read -r format model dataset; do
        if ! test_completed "$format" "$model" "$dataset"; then
            count=$((count + 1))
            printf "%3d. format=%-12s model=%-6s dataset=%s\n" "$count" "$format" "$model" "$dataset"
        fi
    done

    if [[ $count -eq 0 ]]; then
        echo -e "${GREEN}All tests completed!${NC}"
    fi
}

# Run a single test
run_test() {
    local format="$1"
    local model="$2"
    local dataset="$3"

    local dataset_name="${dataset//\//-}"
    local test_id="${format}_${model}_${dataset_name}"

    log "INFO" "Starting test: $test_id"
    echo -e "${YELLOW}Running: format=$format model=$model dataset=$dataset${NC}"

    # Check if already completed
    if test_completed "$format" "$model" "$dataset"; then
        echo -e "${GREEN}✓ Already completed, skipping${NC}"
        log "INFO" "Test $test_id already completed, skipping"
        return 0
    fi

    # Build paths - handle nested datasets
    local data_file
    local prompt_file
    if [[ "$dataset" == *"/"* ]]; then
        local category="${dataset%/*}"
        local name="${dataset#*/}"
        data_file="$ENCODED_DIR/$category/$name.$format"
        prompt_file="$PROMPTS_DIR/$category/$name.json"
    else
        data_file="$ENCODED_DIR/$dataset.$format"
        prompt_file="$PROMPTS_DIR/$dataset.json"
    fi

    # Validate files exist
    if [[ ! -f "$data_file" ]]; then
        echo -e "${RED}✗ Data file not found: $data_file${NC}"
        log "ERROR" "Data file not found: $data_file"
        return 1
    fi

    if [[ ! -f "$prompt_file" ]]; then
        echo -e "${RED}✗ Prompt file not found: $prompt_file${NC}"
        log "ERROR" "Prompt file not found: $prompt_file"
        return 1
    fi

    # Read data
    local data
    data=$(<"$data_file")

    # Extract questions (first 5)
    local questions
    questions=$(jq -r '.questions[] | "Q: \(.q)"' "$prompt_file" | head -5)

    # Build full prompt
    local full_prompt="Here is data:

$data

Answer these questions about the data above:
$questions"

    # Get model name
    local model_name="${MODEL_NAMES[$model]}"

    # Create session directory for this test
    local session_dir="$SESSIONS_DIR/$test_id"
    mkdir -p "$session_dir"

    # Run claude with isolated session
    local start_time=$(date +%s)
    local session_file=""

    # Clear any cached session data that might affect token counts
    rm -rf ~/.claude/projects/*/sessions/* 2>/dev/null || true

    # Run with JSON output format for clean token extraction
    local json_output
    if json_output=$(echo "$full_prompt" | claude --model "$model_name" --print --output-format json --no-session-persistence 2>&1); then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))

        # Save the raw JSON output
        echo "$json_output" > "$session_dir/output.json"

        # Extract ALL token data - store full objects for later analysis
        local timestamp=$(date -Iseconds)
        local result_json=$(echo "$json_output" | jq \
            --arg ts "$timestamp" \
            --arg fmt "$format" \
            --arg mdl "$model" \
            --arg ds "$dataset" \
            --arg dur "$duration" \
            '{
                timestamp: $ts,
                format: $fmt,
                model: $mdl,
                dataset: $ds,
                duration_seconds: ($dur | tonumber),
                duration_ms: .duration_ms,
                duration_api_ms: .duration_api_ms,
                num_turns: .num_turns,
                total_cost_usd: .total_cost_usd,
                usage: .usage,
                model_usage: .modelUsage
            }')

        # Extract summary values for display
        local input_tokens=$(echo "$json_output" | jq -r '.usage.input_tokens // 0')
        local output_tokens=$(echo "$json_output" | jq -r '.usage.output_tokens // 0')
        local cache_creation=$(echo "$json_output" | jq -r '.usage.cache_creation_input_tokens // 0')

        # Append to results file
        echo "$result_json" >> "$RESULTS_FILE"

        echo -e "${GREEN}✓ Complete (${duration}s) - Input: $input_tokens, Output: $output_tokens, Cache: $cache_creation${NC}"
        log "INFO" "Test $test_id completed successfully in ${duration}s"
        return 0
    else
        echo -e "${RED}✗ Claude command failed${NC}"
        log "ERROR" "Claude command failed for $test_id"
        echo "$json_output" | tee -a "$LOG_FILE"
        return 1
    fi
}

# Show usage
show_usage() {
    cat << EOF
${BLUE}Benchmark Runner - Token Efficiency Testing${NC}

Usage:
  $0 --help                                      Show this help
  $0 --list                                      List all possible tests
  $0 --list-remaining                            List tests not yet run
  $0 --all                                       Run ALL tests (105 total!)
  $0 --batch N                                   Run next N untested combinations
  $0 --format FORMAT                             Run all tests for format
  $0 --model MODEL                               Run all tests for model
  $0 --dataset DATASET                           Run all tests for dataset
  $0 --format F --model M --dataset D            Run single specific test

Formats: ${FORMATS[*]}
Models:  ${MODELS[*]}
Datasets: ${DATASETS[*]}

Examples:
  $0 --list-remaining                            # See what's left
  $0 --batch 5                                   # Run next 5 tests
  $0 --format stele-ascii --model sonnet         # All sonnet tests with stele-ascii
  $0 --format json --model opus --dataset flat/100  # Single specific test

Results saved to: $RESULTS_FILE
Logs saved to: $LOG_FILE

NOTE: CLAUDE.md is temporarily removed during benchmarks for clean token counts,
      and automatically restored when the script exits.
EOF
}

# Main execution
main() {
    local filter_format=""
    local filter_model=""
    local filter_dataset=""
    local batch_size=""
    local run_all=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help|-h)
                show_usage
                exit 0
                ;;
            --list)
                list_all
                exit 0
                ;;
            --list-remaining)
                list_remaining
                exit 0
                ;;
            --all)
                run_all=true
                shift
                ;;
            --batch)
                batch_size="$2"
                shift 2
                ;;
            --format)
                filter_format="$2"
                shift 2
                ;;
            --model)
                filter_model="$2"
                shift 2
                ;;
            --dataset)
                filter_dataset="$2"
                shift 2
                ;;
            *)
                echo -e "${RED}Unknown option: $1${NC}"
                show_usage
                exit 1
                ;;
        esac
    done

    # If no args, show usage
    if [[ -z "$filter_format" && -z "$filter_model" && -z "$filter_dataset" && -z "$batch_size" && "$run_all" == "false" ]]; then
        show_usage
        exit 0
    fi

    # Backup CLAUDE.md for clean benchmarks
    backup_claude_md

    log "INFO" "Benchmark run started"

    local tests_run=0
    local tests_failed=0
    local tests_skipped=0

    # Generate and filter test list
    while read -r format model dataset; do
        # Apply filters
        if [[ -n "$filter_format" && "$format" != "$filter_format" ]]; then
            continue
        fi
        if [[ -n "$filter_model" && "$model" != "$filter_model" ]]; then
            continue
        fi
        if [[ -n "$filter_dataset" && "$dataset" != "$filter_dataset" ]]; then
            continue
        fi

        # Check batch limit
        if [[ -n "$batch_size" && $tests_run -ge $batch_size ]]; then
            break
        fi

        # Skip if already completed (for batch mode)
        if [[ -n "$batch_size" ]] && test_completed "$format" "$model" "$dataset"; then
            continue
        fi

        # Run the test (continue on failure)
        set +e
        if run_test "$format" "$model" "$dataset"; then
            tests_run=$((tests_run + 1))
        else
            tests_failed=$((tests_failed + 1))
        fi
        set -e

        echo ""  # Blank line between tests
    done < <(generate_all_tests)

    # Summary
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Benchmark Summary${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}Tests completed: $tests_run${NC}"
    if [[ $tests_failed -gt 0 ]]; then
        echo -e "${RED}Tests failed: $tests_failed${NC}"
    fi

    log "INFO" "Benchmark run completed: $tests_run successful, $tests_failed failed"
}

main "$@"
