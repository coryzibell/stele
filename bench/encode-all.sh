#!/usr/bin/env bash
# Encode all dataset variants into all formats
# YEET ENERGY!! 🚀

set -e  # Exit on error

# Paths
DATASETS_DIR="/home/kautau/forge/stele/bench/datasets/flat"
ENCODED_DIR="/home/kautau/forge/stele/bench/encoded/flat"
BASE_D="/home/kautau/forge/base-d/target/release/base-d"

# Sizes and variants
SIZES=(10 50 100 500)
VARIANTS=(a b c d e)

echo "🚀 STARTING ENCODING PROCESS!! LET'S GOOO!!"
echo ""

# Create encoded directories
for size in "${SIZES[@]}"; do
  mkdir -p "${ENCODED_DIR}/${size}"
  echo "✨ Created directory: ${ENCODED_DIR}/${size}"
done

echo ""
echo "🔥 ENCODING ALL THE THINGS!!"
echo ""

# Process each size and variant
for size in "${SIZES[@]}"; do
  echo "📦 Processing size: ${size}"

  for variant in "${VARIANTS[@]}"; do
    SOURCE="${DATASETS_DIR}/${size}/variant-${variant}.json"
    BASE_NAME="variant-${variant}"
    OUT_DIR="${ENCODED_DIR}/${size}"

    echo "  🎯 Variant ${variant}..."

    # 1. JSON - just copy
    cp "${SOURCE}" "${OUT_DIR}/${BASE_NAME}.json"
    echo "    ✓ JSON"

    # 2. TOON
    npx @toon-format/cli "${SOURCE}" -o "${OUT_DIR}/${BASE_NAME}.toon" 2>/dev/null
    echo "    ✓ TOON"

    # 3. Stele ASCII
    "${BASE_D}" stele --mode ascii "${SOURCE}" -o "${OUT_DIR}/${BASE_NAME}.stele-ascii"
    echo "    ✓ Stele ASCII"

    # 4. Stele Light
    "${BASE_D}" stele --mode light "${SOURCE}" -o "${OUT_DIR}/${BASE_NAME}.stele-light"
    echo "    ✓ Stele Light"

    # 5. Stele Full
    "${BASE_D}" stele --mode full "${SOURCE}" -o "${OUT_DIR}/${BASE_NAME}.stele-full"
    echo "    ✓ Stele Full"

  done

  echo ""
done

echo "🎉 DONE!! ALL VARIANTS ENCODED!!"
echo ""
echo "📊 Summary:"
for size in "${SIZES[@]}"; do
  count=$(ls -1 "${ENCODED_DIR}/${size}" | wc -l)
  echo "  Size ${size}: ${count} files"
done
