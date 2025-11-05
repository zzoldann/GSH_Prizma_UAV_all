#!/usr/bin/env bash
set -Eeuo pipefail
shopt -s extglob
trap 'st=$?; echo "[ERR] ${BASH_SOURCE[0]}:${LINENO} cmd: ${BASH_COMMAND} (exit=$st)"; exit $st' ERR

MODE="${MODE:-pyinstaller}"
PKGNAME="gsh-prizma-gen3"
OUT="builder-kit/out"

VERSION="$(python3 - <<'PY'
import pathlib,re,sys
p=pathlib.Path('src')/'gsh_prizma'/'__init__.py'
s=p.read_text(encoding='utf-8') if p.exists() else ''
import re
m=re.search(r"__version__\s*=\s*['\"](.+?)['\"]", s)
print(m.group(1) if m else '0.0.0')
PY
)"
: "${VERSION:?version-read-failed}"
echo "[i] Version: $VERSION"
echo "[i] Mode   : $MODE"

ensure_fpm() {
  if ! command -v fpm >/dev/null 2>&1; then
    echo "[i] Installing fpm via apt+gem (sudo required)…"
    sudo apt update
    sudo apt install -y ruby ruby-dev build-essential rpm
    sudo gem install --no-document fpm
  fi
}

build_pyinstaller() {
  local BIN_ONEFILE="dist/gsh-prizma-gen3"
  local BIN_ONEFOLDER="dist/gsh-prizma-gen3/gsh-prizma-gen3"
  [[ -x "$BIN_ONEFILE" || -x "$BIN_ONEFOLDER" ]] && return 0
  local PY=python3 PIP=pip
  if [[ -n "${VIRTUAL_ENV:-}" ]]; then
    PY="$VIRTUAL_ENV/bin/python"; PIP="$VIRTUAL_ENV/bin/pip"
  else
    local VENV="builder-kit/.pyi-venv"
    [[ -x "$VENV/bin/python" ]] || python3 -m venv "$VENV"
    PY="$VENV/bin/python"; PIP="$VENV/bin/pip"
    "$PIP" install -r builder-kit/requirements.txt
  fi
  "$PY" -m PyInstaller --noconfirm builder-kit/gsh_prizma_gui.spec
}

ensure_fpm
WORK="builder-kit/.build-rpm"
rm -rf "$WORK"; mkdir -p "$WORK" "$OUT"

declare -a DEPENDS=()

if [[ "$MODE" == "pyinstaller" ]]; then
  build_pyinstaller
  BIN=""
  [[ -x dist/gsh-prizma-gen3 ]] && BIN="dist/gsh-prizma-gen3"
  [[ -z "$BIN" && -x dist/gsh-prizma-gen3/gsh-prizma-gen3 ]] && BIN="dist/gsh-prizma-gen3/gsh-prizma-gen3"
  [[ -n "$BIN" ]] || { echo "[!] PyInstaller binary not found in dist/"; exit 1; }
  echo "[i] Using binary: $BIN"
  install -d "$WORK/usr/bin"
  install -m 0755 "$BIN" "$WORK/usr/bin/gsh-prizma-gen3"
  [[ -f assets/help/help_ru.json ]] || { mkdir -p assets/help; printf '{}' > assets/help/help_ru.json; }
  install -d "$WORK/usr/share/${PKGNAME}/help"
  install -m 0644 assets/help/help_ru.json "$WORK/usr/share/${PKGNAME}/help/help_ru.json"
else
  install -d "$WORK/usr/share/${PKGNAME}"
  rsync -a --exclude '__pycache__' src assets "$WORK/usr/share/${PKGNAME}/"
  install -d "$WORK/usr/bin"
  cat > "$WORK/usr/bin/gsh-prizma-gen3" <<'LAUNCH'
#!/usr/bin/env bash
set -euo pipefail
ROOT="/usr/share/gsh-prizma-gen3"
export PYTHONPATH="$ROOT/src:$PYTHONPATH"
exec python3 -m gsh_prizma
LAUNCH
  chmod +x "$WORK/usr/bin/gsh-prizma-gen3"
  DEPENDS+=(--depends "python3" --depends "python3-pyside6")
fi

FPM_ARGS=(
  -s dir -t rpm
  -n "$PKGNAME" -v "$VERSION"
  --license MIT --architecture x86_64
  --description "GSH Prizma Gen3 CDSA UAV (GUI) — v$VERSION"
  --url "https://example.local/gsh-prizma"
  --maintainer "GSH Team <noreply@example.local>"
  --force
  -p "$OUT"
)
if ((${#DEPENDS[@]})); then FPM_ARGS+=("${DEPENDS[@]}"); fi
FPM_ARGS+=( -C "$WORK" usr/bin/gsh-prizma-gen3 usr/share/$PKGNAME/help/help_ru.json )

echo "[i] fpm ${FPM_ARGS[*]}"
fpm "${FPM_ARGS[@]}"

echo "[✓] Built .rpm -> $OUT"
ls -lh "$OUT"/${PKGNAME}-*.rpm
