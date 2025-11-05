#!/usr/bin/env bash
set -euo pipefail
which fpm >/dev/null || { echo "Install fpm: sudo dnf install -y ruby-devel gcc make && sudo gem install --no-document fpm"; exit 1; }

VER="$(python3 - <<'PY'
import tomllib,sys
with open("pyproject.toml","rb") as f: data=tomllib.load(f)
print(data["project"]["version"])
PY
)"
NAME="gsh-prizma-cdsa"
APPDIR="opt/gsh_prizma_cdsauav-$VER"
STAGE="build/pkgroot"
rm -rf "$STAGE"; mkdir -p "$STAGE/$APPDIR"

python -m pip install -U build >/dev/null
rm -f dist/gsh_prizma_cdsauav-*.whl
python -m build

rsync -a --exclude ".venv" --exclude "__pycache__" --exclude ".git" \
  src examples tools packaging run_dev_verbose.sh README.md BUILD.md CHANGELOG.md LICENSE dist \
  "$STAGE/$APPDIR/"

sed "s/__VER__/$VER/g" packaging/postinstall.sh > "$STAGE/$APPDIR/postinstall.sh"
sed "s/__VER__/$VER/g" packaging/prerm.sh       > "$STAGE/$APPDIR/prerm.sh"
chmod +x "$STAGE/$APPDIR/"*.sh

fpm -s dir -t rpm \
  -n "$NAME" -v "$VER" --architecture all \
  --description "GSH Prizma Gen3 CDSA UAV (GUI) — link budget + Hata/COST-231 + Antenna Wizard Lite" \
  --license "MIT" \
  --depends "python3 >= 3.10" \
  --after-install "$STAGE/$APPDIR/postinstall.sh" \
  --before-remove "$STAGE/$APPDIR/prerm.sh" \
  -C "$STAGE" \
  "$APPDIR"

echo "[OK] .rpm готов."
