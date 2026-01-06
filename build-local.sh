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

    echo "=== Building $shield ($shield_name) ==="

    west build -s zmk/app -b eyelash_nano -d "$build_dir" -- \
        -DZephyr_DIR="${PROJ_DIR}/zephyr/share/zephyr-package/cmake" \
        -DSHIELD="$shield_name" \
        -DZMK_CONFIG="${PROJ_DIR}/config" \
        -DZMK_EXTRA_MODULES="${PROJ_DIR}/boards"

    echo "✓ Built: ${build_dir}/zephyr/zmk.uf2"
}

case "${1:-all}" in
    left)
        build_shield left "offsetkey_peripheral_left"
        ;;
    right)
        build_shield right "offsetkey_peripheral_right"
        ;;
    dongle)
        build_shield dongle "offsetkey_central_dongle"
        ;;
    all)
        build_shield left "offsetkey_peripheral_left"
        build_shield right "offsetkey_peripheral_right"
        build_shield dongle "offsetkey_central_dongle"
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
