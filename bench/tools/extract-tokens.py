#!/usr/bin/env python3
"""
Extract token counts from Claude session JSONL files.

Reads a session file and outputs token usage as JSON.
"""

import json
import sys
from pathlib import Path


def extract_tokens(session_file: Path) -> dict:
    """Extract token counts from session JSONL file."""

    if not session_file.exists():
        raise FileNotFoundError(f"Session file not found: {session_file}")

    input_tokens = 0
    output_tokens = 0
    cache_read_tokens = 0
    cache_creation_tokens = 0

    # Read session file line by line
    with session_file.open('r') as f:
        for line in f:
            try:
                event = json.loads(line.strip())

                # Look for message events with usage data
                if event.get('type') == 'message':
                    usage = event.get('usage', {})

                    # Accumulate token counts
                    input_tokens += usage.get('input_tokens', 0)
                    output_tokens += usage.get('output_tokens', 0)
                    cache_read_tokens += usage.get('cache_read_input_tokens', 0)
                    cache_creation_tokens += usage.get('cache_creation_input_tokens', 0)

            except json.JSONDecodeError:
                # Skip invalid JSON lines
                continue

    return {
        'input_tokens': input_tokens,
        'output_tokens': output_tokens,
        'cache_read_tokens': cache_read_tokens,
        'cache_creation_tokens': cache_creation_tokens,
    }


def main():
    if len(sys.argv) != 2:
        print("Usage: extract-tokens.py <session-file.jsonl>", file=sys.stderr)
        sys.exit(1)

    session_file = Path(sys.argv[1])

    try:
        tokens = extract_tokens(session_file)
        print(json.dumps(tokens, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
