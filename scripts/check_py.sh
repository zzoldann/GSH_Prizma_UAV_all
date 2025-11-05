#!/usr/bin/env bash
set -euo pipefail
python -m compileall -q src
echo "[OK] py_compile passed"
