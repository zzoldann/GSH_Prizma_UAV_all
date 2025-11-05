#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v fpm >/dev/null 2>&1; then
  echo "[!] fpm not found. Install: sudo gem install --no-document fpm"
  exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "[!] python3 not found"; exit 1
fi

test -d dist || mkdir -p dist
if ! ls dist/gsh_prizma_cdsauav-*.whl >/dev/null 2>&1; then
  python3 -m pip install --upgrade build >/dev/null 2>&1 || true
  python3 -m build -w
fi

WHEEL="$(ls -1 dist/gsh_prizma_cdsauav-*.whl | head -n1)"
VER="$(python3 - <<'PY'
import tomllib, pathlib
d = tomllib.loads(pathlib.Path('pyproject.toml').read_bytes())
print(d['project']['version'])
PY
)"
NAME="gsh-prizma-cdsauav"

fpm -s python -t deb "$WHEEL"     --name "$NAME"     --version "$VER"     --python-bin python3     -d "python3 (>= 3.9)"     -d "python3-pyside6.qtcore"     -d "python3-pyside6.qtgui"     -d "python3-pyside6.qtwidgets"     -d "python3-matplotlib"

echo "[i] Done. See *.deb in $(pwd)"
