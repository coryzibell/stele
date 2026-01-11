#!/usr/bin/env python3
"""
Aggregate token results into summary report.

Usage:
    aggregate.py <results-dir>

Reads token-counts.json entries and produces:
- results/summary.md - Human readable tables
- results/comparison.json - Machine readable results

Expected structure:
    results-dir/
        flat-10-json/token-counts.json
        flat-10-ascii/token-counts.json
        flat-10-light/token-counts.json
        flat-10-full/token-counts.json
        ...
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List
from collections import defaultdict


def parse_dir_name(dirname: str) -> tuple:
    """
    Parse directory name into (dataset, format).

    Examples:
        'flat-10-json' -> ('flat/10', 'json')
        'nested-100-ascii' -> ('nested/100', 'ascii')
    """

    parts = dirname.split('-')
    if len(parts) < 3:
        return None, None

    dataset_type = parts[0]  # flat, nested, deep
    dataset_size = parts[1]   # 10, 100, 1000
    format_name = '-'.join(parts[2:])  # json, ascii, light, full

    dataset = f"{dataset_type}/{dataset_size}"

    return dataset, format_name


def load_results(results_dir: Path) -> Dict[str, Dict[str, Any]]:
    """
    Load all token-counts.json files from results directory.

    Returns dict mapping (dataset, format) -> token counts
    """

    results = defaultdict(dict)

    for subdir in results_dir.iterdir():
        if not subdir.is_dir():
            continue

        token_file = subdir / 'token-counts.json'
        if not token_file.exists():
            print(f"Warning: No token-counts.json in {subdir.name}", file=sys.stderr)
            continue

        dataset, format_name = parse_dir_name(subdir.name)
        if not dataset or not format_name:
            print(f"Warning: Could not parse directory name: {subdir.name}",
                  file=sys.stderr)
            continue

        try:
            with open(token_file, 'r') as f:
                data = json.load(f)
                results[dataset][format_name] = data
        except Exception as e:
            print(f"Warning: Error reading {token_file}: {e}", file=sys.stderr)
            continue

    return dict(results)


def format_number(n: int) -> str:
    """Format number with commas for readability."""
    return f"{n:,}"


def generate_markdown_table(results: Dict[str, Dict[str, Any]],
                            metric: str = 'total_all') -> str:
    """
    Generate markdown comparison table.

    metric: which token count to compare (total_all, input_tokens, etc)
    """

    # Get all datasets and formats
    datasets = sorted(results.keys())

    if not datasets:
        return "No results found.\n"

    # Determine available formats from first dataset
    formats = ['json', 'ascii', 'light', 'full']
    available_formats = []

    for fmt in formats:
        if any(fmt in results[ds] for ds in datasets):
            available_formats.append(fmt)

    if not available_formats:
        return "No format data found.\n"

    # Build table
    lines = []

    # Header
    header = "| Dataset | " + " | ".join(f.capitalize() for f in available_formats) + " |"
    separator = "|---------|" + "|".join("--------" for _ in available_formats) + "|"

    lines.append(header)
    lines.append(separator)

    # Rows
    for dataset in datasets:
        row_data = [dataset]

        for fmt in available_formats:
            if fmt in results[dataset]:
                value = results[dataset][fmt].get(metric, 0)
                row_data.append(format_number(value))
            else:
                row_data.append("-")

        row = "| " + " | ".join(row_data) + " |"
        lines.append(row)

    return "\n".join(lines)


def generate_summary(results: Dict[str, Dict[str, Any]]) -> str:
    """Generate complete summary markdown."""

    sections = [
        "# Token Usage Comparison",
        "",
        "## Total Tokens (All Sources)",
        "",
        generate_markdown_table(results, 'total_all'),
        "",
        "## Input Tokens (Non-Cached)",
        "",
        generate_markdown_table(results, 'input_tokens'),
        "",
        "## Cache Read Tokens",
        "",
        generate_markdown_table(results, 'cache_read_input_tokens'),
        "",
        "## Output Tokens",
        "",
        generate_markdown_table(results, 'output_tokens'),
        "",
    ]

    return "\n".join(sections)


def generate_comparison_json(results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Generate machine-readable comparison data."""

    comparison = {
        'datasets': {},
        'summary': {
            'formats': ['json', 'ascii', 'light', 'full'],
            'metrics': ['input_tokens', 'cache_read_input_tokens',
                       'cache_creation_input_tokens', 'output_tokens',
                       'total_input', 'total_all']
        }
    }

    for dataset, formats in results.items():
        comparison['datasets'][dataset] = formats

    return comparison


def main():
    """Main entry point."""

    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0 if len(sys.argv) >= 2 else 1)

    results_dir = Path(sys.argv[1])

    if not results_dir.exists():
        print(f"Error: Directory not found: {results_dir}", file=sys.stderr)
        sys.exit(1)

    if not results_dir.is_dir():
        print(f"Error: Not a directory: {results_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading results from {results_dir}...")
    results = load_results(results_dir)

    if not results:
        print("Error: No valid results found", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(results)} datasets")

    # Generate summary markdown
    summary_file = results_dir / 'summary.md'
    summary_md = generate_summary(results)

    with open(summary_file, 'w') as f:
        f.write(summary_md)

    print(f"Wrote summary to {summary_file}")

    # Generate comparison JSON
    comparison_file = results_dir / 'comparison.json'
    comparison_data = generate_comparison_json(results)

    with open(comparison_file, 'w') as f:
        json.dump(comparison_data, f, indent=2)

    print(f"Wrote comparison to {comparison_file}")

    print("\nDone! 🚀")


if __name__ == '__main__':
    main()
