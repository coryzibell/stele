#!/usr/bin/env bash
# Show benchmark progress - quick status overview

set -euo pipefail

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Paths
BENCH_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESULTS_FILE="$BENCH_DIR/results/token-counts.jsonl"

# Total tests: 5 formats × 3 models × 7 datasets = 105
TOTAL_TESTS=105

# Count completed tests
if [[ -f "$RESULTS_FILE" ]]; then
    COMPLETED=$(wc -l < "$RESULTS_FILE")
else
    COMPLETED=0
fi

REMAINING=$((TOTAL_TESTS - COMPLETED))
PERCENT=$((COMPLETED * 100 / TOTAL_TESTS))

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Benchmark Progress${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}Completed:${NC} $COMPLETED / $TOTAL_TESTS tests ($PERCENT%)"
echo -e "${YELLOW}Remaining:${NC} $REMAINING tests"
echo ""

# Show progress bar
BAR_WIDTH=50
FILLED=$((COMPLETED * BAR_WIDTH / TOTAL_TESTS))
EMPTY=$((BAR_WIDTH - FILLED))

printf "["
printf "%${FILLED}s" | tr ' ' '='
printf "%${EMPTY}s" | tr ' ' '-'
printf "] %d%%\n" "$PERCENT"

echo ""

# Show breakdown by format if results exist
if [[ -f "$RESULTS_FILE" && -s "$RESULTS_FILE" ]]; then
    echo -e "${BLUE}Breakdown by format:${NC}"
    for format in json stele-ascii stele-light stele-full toon; do
        count=$(grep -c "\"format\":\"$format\"" "$RESULTS_FILE" || echo 0)
        printf "  %-12s: %2d / 21 tests\n" "$format" "$count"
    done
    echo ""

    echo -e "${BLUE}Breakdown by model:${NC}"
    for model in opus sonnet haiku; do
        count=$(grep -c "\"model\":\"$model\"" "$RESULTS_FILE" || echo 0)
        printf "  %-6s: %2d / 35 tests\n" "$model" "$count"
    done
fi

echo ""
echo -e "${BLUE}========================================${NC}"
