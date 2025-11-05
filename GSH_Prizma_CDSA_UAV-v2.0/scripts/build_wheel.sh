#!/usr/bin/env bash
set -euo pipefail
rm -rf dist && mkdir -p dist
python -m pip install -U build
python -m build
