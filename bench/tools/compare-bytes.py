#!/usr/bin/env python3
"""
Compare byte sizes across all encoded formats.

Usage:
    compare-bytes.py <encoded-dir>

Outputs byte comparison table for all datasets.

Expected structure:
    encoded-dir/
        flat/
            10.json
            10.stele-ascii
            10.stele-light
            10.stele-full
"""

import sys
from pathlib import Path
from typing import Dict, List


def get_file_size(filepath: Path) -> int:
    """Get file size in bytes, return 0 if file doesn't exist."""
    try:
        return filepath.stat().st_size
    except FileNotFoundError:
        return 0


def collect_sizes(encoded_dir: Path) -> Dict[str, Dict[str, int]]:
    """
    Collect file sizes for all datasets and formats.

    Returns dict mapping dataset -> format -> bytes
    """

    sizes = {}

    # Expected structure: type/size.json, type/size.stele-*
    for type_dir in encoded_dir.iterdir():
        if not type_dir.is_dir():
            continue

        # Get all JSON files in this directory
        json_files = list(type_dir.glob("*.json"))

        for json_file in json_files:
            # Extract size from filename (e.g., "10.json" -> "10")
            size_name = json_file.stem

            dataset = f"{type_dir.name}/{size_name}"

            # Check for all format files
            formats = {
                'json': json_file,
                'ascii': type_dir / f"{size_name}.stele-ascii",
                'light': type_dir / f"{size_name}.stele-light",
                'full': type_dir / f"{size_name}.stele-full"
            }

            dataset_sizes = {}
            for fmt, filepath in formats.items():
                size = get_file_size(filepath)
                if size > 0:  # Only include if file exists
                    dataset_sizes[fmt] = size

            if dataset_sizes:  # Only add dataset if it has files
                sizes[dataset] = dataset_sizes

    return sizes


def format_bytes(b: int) -> str:
    """Format bytes with comma separators."""
    return f"{b:,}"


def calculate_reduction(baseline: int, compressed: int) -> str:
    """Calculate percentage reduction from baseline."""
    if baseline == 0:
        return "-"
    reduction = ((baseline - compressed) / baseline) * 100
    return f"{reduction:+.1f}%"


def generate_table(sizes: Dict[str, Dict[str, int]]) -> str:
    """Generate markdown table comparing byte sizes."""

    if not sizes:
        return "No data found.\n"

    datasets = sorted(sizes.keys())
    formats = ['json', 'ascii', 'light', 'full']

    lines = []

    # Header
    header = "| Dataset | JSON | ASCII | Light | Full |"
    separator = "|---------|------|-------|-------|------|"

    lines.append(header)
    lines.append(separator)

    # Rows
    for dataset in datasets:
        row_data = [dataset]
        json_size = sizes[dataset].get('json', 0)

        for fmt in formats:
            if fmt in sizes[dataset]:
                size = sizes[dataset][fmt]

                if fmt == 'json':
                    # Just show size for baseline
                    row_data.append(format_bytes(size))
                else:
                    # Show size and reduction from JSON
                    reduction = calculate_reduction(json_size, size)
                    row_data.append(f"{format_bytes(size)} ({reduction})")
            else:
                row_data.append("-")

        row = "| " + " | ".join(row_data) + " |"
        lines.append(row)

    return "\n".join(lines)


def generate_summary(sizes: Dict[str, Dict[str, int]]) -> str:
    """Generate summary statistics."""

    if not sizes:
        return ""

    # Calculate averages across all datasets
    format_totals = {'json': [], 'ascii': [], 'light': [], 'full': []}

    for dataset_sizes in sizes.values():
        for fmt, size in dataset_sizes.items():
            format_totals[fmt].append(size)

    lines = [
        "",
        "## Summary Statistics",
        "",
        "Average file sizes:",
        ""
    ]

    json_avg = sum(format_totals['json']) / len(format_totals['json']) if format_totals['json'] else 0

    for fmt in ['json', 'ascii', 'light', 'full']:
        if format_totals[fmt]:
            avg = sum(format_totals[fmt]) / len(format_totals[fmt])

            if fmt == 'json':
                lines.append(f"- **{fmt.upper()}**: {format_bytes(int(avg))} bytes")
            else:
                reduction = calculate_reduction(int(json_avg), int(avg))
                lines.append(f"- **{fmt.upper()}**: {format_bytes(int(avg))} bytes ({reduction} vs JSON)")

    return "\n".join(lines)


def main():
    """Main entry point."""

    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0 if len(sys.argv) >= 2 else 1)

    encoded_dir = Path(sys.argv[1])

    if not encoded_dir.exists():
        print(f"Error: Directory not found: {encoded_dir}", file=sys.stderr)
        sys.exit(1)

    if not encoded_dir.is_dir():
        print(f"Error: Not a directory: {encoded_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {encoded_dir} for encoded files...")
    sizes = collect_sizes(encoded_dir)

    if not sizes:
        print("Error: No encoded files found", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(sizes)} datasets\n")

    # Generate and print table
    print("# Byte Size Comparison")
    print()
    table = generate_table(sizes)
    print(table)

    # Print summary
    summary = generate_summary(sizes)
    print(summary)

    print("\n✨ Done!")


if __name__ == '__main__':
    main()
