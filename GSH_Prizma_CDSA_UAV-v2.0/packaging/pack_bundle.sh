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

python3 -m pip install --upgrade build >/dev/null 2>&1 || true
python3 -m build -w
WHEEL="$(ls -1 dist/gsh_prizma_cdsauav-*.whl | head -n1)"

VER="$(python3 - <<'PY'
import tomllib, pathlib
d = tomllib.loads(pathlib.Path('pyproject.toml').read_bytes())
print(d['project']['version'])
PY
)"
NAME="gsh-prizma-cdsauav"
PKGROOT="$(mktemp -d)"
install -d "$PKGROOT/opt/gsh-prizma" "$PKGROOT/usr/bin"

python3 -m venv "$PKGROOT/opt/gsh-prizma/venv"
source "$PKGROOT/opt/gsh-prizma/venv/bin/activate"
python -m pip install --upgrade pip
python -m pip install "$WHEEL" PySide6 matplotlib

cat > "$PKGROOT/usr/bin/prizma-cdsa" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
APPDIR="/opt/gsh-prizma"
source "$APPDIR/venv/bin/activate"
exec python -m gsh_prizma.cli "$@"
SH
chmod +x "$PKGROOT/usr/bin/prizma-cdsa"

install -d "$PKGROOT/usr/share/applications"
cat > "$PKGROOT/usr/share/applications/gsh-prizma.desktop" <<'DESK'
[Desktop Entry]
Name=GSH Prizma Gen3 CDSA UAV
Exec=prizma-cdsa gui
Type=Application
Categories=Science;Engineering;
Terminal=false
DESK

fpm -s dir -t deb -n "$NAME" -v "$VER" --description "GSH Prizma Gen3 CDSA UAV (self-contained)" -C "$PKGROOT" .
fpm -s dir -t rpm -n "$NAME" -v "$VER" --description "GSH Prizma Gen3 CDSA UAV (self-contained)" -C "$PKGROOT" .

echo "[i] Built self-contained packages in $(pwd)"
