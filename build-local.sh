#!/bin/bash
# Local ZMK build script for Offsetkey keyboard (Dongle setup)
# Usage: ./build-local.sh [left|right|dongle|all]
set -e

cd "$(dirname "$0")"
PROJ_DIR="$(pwd)"

# Activate virtual environment
source .venv/bin/activate

build_shield() {
    local shield=$1
    local shield_name=$2
    local build_dir="build_${shield}"
    local extra_modules=$3

    echo "=== Building $shield ($shield_name) ==="

    west build -s zmk/app -b eyelash_nano -d "$build_dir" -- \
        -DZephyr_DIR="${PROJ_DIR}/zephyr/share/zephyr-package/cmake" \
        -DSHIELD="$shield_name" \
        -DZMK_CONFIG="${PROJ_DIR}/config" \
        -DZMK_EXTRA_MODULES="$extra_modules"

    echo "✓ Built: ${build_dir}/zephyr/zmk.uf2"
}

# Common modules for all builds
BASE_MODULES="${PROJ_DIR}/boards;${PROJ_DIR}/zmk-pmw3610-cpi"

# Peripheral builds use zmk-offsetkey-status for their display
PERIPHERAL_MODULES="${BASE_MODULES};${PROJ_DIR}/zmk-offsetkey-status"

# Dongle uses zmk-dongle-display for its custom display
DONGLE_MODULES="${BASE_MODULES};${PROJ_DIR}/zmk-dongle-display"

case "${1:-all}" in
    left)
        build_shield left "offsetkey_peripheral_left" "$PERIPHERAL_MODULES"
        ;;
    right)
        build_shield right "offsetkey_peripheral_right" "$PERIPHERAL_MODULES"
        ;;
    dongle)
        build_shield dongle "offsetkey_central_dongle dongle_display" "$DONGLE_MODULES"
        ;;
    all)
        build_shield left "offsetkey_peripheral_left" "$PERIPHERAL_MODULES"
        build_shield right "offsetkey_peripheral_right" "$PERIPHERAL_MODULES"
        build_shield dongle "offsetkey_central_dongle dongle_display" "$DONGLE_MODULES"
        echo ""
        echo "=== Build complete ==="
        echo "Left:   build_left/zephyr/zmk.uf2"
        echo "Right:  build_right/zephyr/zmk.uf2"
        echo "Dongle: build_dongle/zephyr/zmk.uf2"
        ;;
    *)
        echo "Usage: $0 [left|right|dongle|all]"
        exit 1
        ;;
esac
