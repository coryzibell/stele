#!/usr/bin/env bash
# Encode all nested variants to various formats

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATASETS_DIR="$SCRIPT_DIR"
ENCODED_DIR="$(dirname "$SCRIPT_DIR")/../encoded/nested"
BASE_D="$HOME/forge/base-d/target/release/base-d"

DEPTHS=("shallow" "medium" "deep")
VARIANTS=("a" "b" "c" "d" "e")

for depth in "${DEPTHS[@]}"; do
    echo "Processing $depth..."

    for variant in "${VARIANTS[@]}"; do
        src="$DATASETS_DIR/$depth/variant-$variant.json"
        dst_base="$ENCODED_DIR/$depth/variant-$variant"

        # Copy JSON
        cp "$src" "$dst_base.json"

        # Encode to TOON
        npx @toon-format/cli "$src" -o "$dst_base.toon" 2>/dev/null

        # Encode to stele variants
        "$BASE_D" stele --mode ascii < "$src" > "$dst_base.stele-ascii"
        "$BASE_D" stele --mode light < "$src" > "$dst_base.stele-light"
        "$BASE_D" stele --mode full < "$src" > "$dst_base.stele-full"

        echo "  Encoded variant-$variant"
    done
done

echo ""
echo "Done. Encoded $(( ${#DEPTHS[@]} * ${#VARIANTS[@]} * 5 )) files total."
