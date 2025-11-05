#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(pwd)"
NAME="GSH_Prizma_Gen3_CDSA_UAV-v1.2.5-src"
ZIP="${NAME}.zip"
echo "[i] Creating $ZIP"
rm -f "$ZIP"
zip -r -9 "$ZIP"   README.md CHANGELOG.md BUILD.md LICENSE   src assets builder-kit examples scripts -x '**/__pycache__/*'
sha256sum "$ZIP" | tee "SHA256SUMS_v1.2.5.txt"
echo "[✓] Done"
