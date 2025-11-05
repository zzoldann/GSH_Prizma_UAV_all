#!/usr/bin/env bash
# Simple dev launcher
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH="$PWD/src${PYTHONPATH:+:$PYTHONPATH}"
exec python3 -m gsh_prizma "$@"
