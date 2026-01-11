# Benchmark Tools

This directory contains scripts for running token efficiency benchmarks.

## Scripts

### `run-benchmark.sh`

Main benchmark runner with incremental persistence and resume capability.

**Features:**
- Saves results after EACH test (session limit safe)
- Resume capability - tracks completed tests
- Filter by format, model, or dataset
- Batch mode for controlled runs
- Detailed logging

**Quick start:**
```bash
# See what needs to be run
./run-benchmark.sh --list-remaining

# Run next 5 tests
./run-benchmark.sh --batch 5

# Run all tests for a specific format
./run-benchmark.sh --format stele-ascii

# Run a single specific test
./run-benchmark.sh --format json --model sonnet --dataset flat/100
```

### `show-progress.sh`

Quick progress overview showing completed vs remaining tests.

```bash
./show-progress.sh
```

### `extract-tokens.py`

Python utility to extract token counts from Claude session JSONL files.

```bash
./extract-tokens.py path/to/session.jsonl
```

## Output Files

- `results/token-counts.jsonl` - One JSON object per test (append-only)
- `results/benchmark.log` - Detailed execution log
- `sessions/{test-id}/` - Session files and outputs for each test

## Test Matrix

- **Formats:** json, stele-ascii, stele-light, stele-full, toon (5)
- **Models:** opus, sonnet, haiku (3)
- **Datasets:** flat/10, flat/50, flat/100, flat/500, nested/shallow, nested/medium, nested/deep (7)
- **Total:** 5 × 3 × 7 = **105 tests**

## Example Workflow

```bash
# Check progress
./show-progress.sh

# Run a batch
./run-benchmark.sh --batch 10

# Check again
./show-progress.sh

# Run all remaining tests for a format
./run-benchmark.sh --format stele-light --list-remaining
./run-benchmark.sh --format stele-light
```

## Safety Features

- Results saved incrementally (never lose progress)
- Tests can be resumed after interruption
- Failed tests logged but don't stop the run
- Session files preserved for debugging
