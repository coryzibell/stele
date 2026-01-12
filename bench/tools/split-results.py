#!/usr/bin/env python3
"""
Split the monolithic token-counts.jsonl into separate files by model and dataset.

Creates files like:
  results/haiku-flat-10.jsonl
  results/haiku-flat-50.jsonl
  results/opus-nested-deep.jsonl
  etc.

Usage:
  ./split-results.py                     # Split existing data
  ./split-results.py --dry-run           # Show what would be created
"""

import json
import subprocess
import sys
from pathlib import Path
from collections import defaultdict

BENCH_DIR = Path(__file__).parent.parent
RESULTS_DIR = BENCH_DIR / "results"
SOURCE_FILE = RESULTS_DIR / "token-counts.jsonl"


def parse_jsonl_with_jq(filepath: Path) -> list[dict]:
    """Use jq to parse the pretty-printed JSONL file into compact objects."""
    result = subprocess.run(
        ["jq", "-c", ".", str(filepath)],
        capture_output=True,
        text=True,
        check=True
    )

    objects = []
    for line in result.stdout.strip().split("\n"):
        if line:
            objects.append(json.loads(line))
    return objects


def get_output_filename(obj: dict) -> str:
    """Generate output filename from model and dataset.

    e.g., model="haiku", dataset="flat/10" -> "haiku-flat-10.jsonl"
    """
    model = obj.get("model", "unknown")
    dataset = obj.get("dataset", "unknown").replace("/", "-")
    return f"{model}-{dataset}.jsonl"


def split_results(dry_run: bool = False) -> dict[str, int]:
    """Split the monolithic results file into per-model-dataset files.

    Returns a dict of filename -> entry count.
    """
    if not SOURCE_FILE.exists():
        print(f"Source file not found: {SOURCE_FILE}", file=sys.stderr)
        return {}

    print(f"Parsing {SOURCE_FILE}...")
    objects = parse_jsonl_with_jq(SOURCE_FILE)
    print(f"Found {len(objects)} entries")

    # Group by output filename
    grouped: dict[str, list[dict]] = defaultdict(list)
    for obj in objects:
        filename = get_output_filename(obj)
        grouped[filename].append(obj)

    # Write out (or report in dry-run mode)
    counts = {}
    for filename, entries in sorted(grouped.items()):
        filepath = RESULTS_DIR / filename
        counts[filename] = len(entries)

        if dry_run:
            print(f"  Would create: {filename} ({len(entries)} entries)")
        else:
            # Write as compact single-line JSONL (one object per line)
            with open(filepath, "w") as f:
                for entry in entries:
                    f.write(json.dumps(entry) + "\n")
            print(f"  Created: {filename} ({len(entries)} entries)")

    return counts


def main():
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("=== DRY RUN ===")

    counts = split_results(dry_run=dry_run)

    if counts:
        total = sum(counts.values())
        print(f"\nTotal: {len(counts)} files, {total} entries")

        if not dry_run:
            print(f"\nOriginal file preserved: {SOURCE_FILE}")
            print("You can delete it manually after verifying the split files.")


if __name__ == "__main__":
    main()
