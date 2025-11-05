#!/usr/bin/env bash
set -euo pipefail
trap 'st=$?; echo "[ERR] ${BASH_SOURCE[0]}:${LINENO} cmd: ${BASH_COMMAND} (exit=$st)"; exit $st' ERR
ROOT="$(pwd)"
NAME_BASE="GSH_Prizma-v"
VERSION="$(python3 - <<'PY'
import pathlib,re
p=pathlib.Path('src')/'gsh_prizma'/'__init__.py'
s=p.read_text(encoding='utf-8') if p.exists() else ''
m=re.search(r"__version__\s*=\s*['\"](.+?)['\"]", s)
print(m.group(1) if m else '0.0.0')
PY
)"
RELEASE="${NAME_BASE}${VERSION}"
STAGE="builder-kit/.srcstage"
OUT="builder-kit/out"
mkdir -p "$STAGE" "$OUT"
echo "[i] Release: $RELEASE"
rm -rf "$STAGE"; mkdir -p "$STAGE"
rsync -a --exclude '__pycache__' src "$STAGE/"
test -d assets   && rsync -a --exclude '__pycache__' assets "$STAGE/"   || true
test -d examples && rsync -a --exclude '__pycache__' examples "$STAGE/" || true
for f in README.md CHANGELOG.md LICENSE BUILD.md; do
  test -f "$f" && install -m 0644 "$f" "$STAGE/$f" || true
done
install -d "$STAGE/builder-kit"
for f in builder-kit/gsh_prizma_gui.spec builder-kit/requirements.txt; do
  test -f "$f" && install -m 0644 "$f" "$STAGE/$f" || true
done
for f in builder-kit/pack_deb.sh builder-kit/pack_rpm.sh builder-kit/smoke_test.sh builder-kit/make_src_release.sh; do
  test -f "$f" && install -m 0755 "$f" "$STAGE/$f" || true
done
rm -rf "$STAGE"/dist "$STAGE"/build "$STAGE"/.venv
HDR="docs/README_HEADER_v${VERSION}.md"
BLK="docs/CHANGELOG_v${VERSION}_block.md"
if [[ -f "$HDR" && -f "$STAGE/README.md" ]] && ! grep -q "v${VERSION}" "$STAGE/README.md"; then
  cp "$STAGE/README.md" "$STAGE/README.md.bak"
  cat "$HDR" "$STAGE/README.md.bak" > "$STAGE/README.md"
fi
if [[ -f "$BLK" && -f "$STAGE/CHANGELOG.md" ]] && ! grep -q "v${VERSION}" "$STAGE/CHANGELOG.md"; then
  cp "$STAGE/CHANGELOG.md" "$STAGE/CHANGELOG.md.bak"
  cat "$BLK" "$STAGE/CHANGELOG.md.bak" > "$STAGE/CHANGELOG.md"
fi
ZIP="${ROOT}/${OUT}/${RELEASE}-src.zip"
( cd "$STAGE" && zip -qr "$ZIP" . )
echo "[✓] ZIP: $ZIP"
( cd "${ROOT}/${OUT}" && sha256sum "$(basename "$ZIP")" > "SHA256SUMS_v${VERSION}.txt" )
echo "[✓] SHA256: ${ROOT}/${OUT}/SHA256SUMS_v${VERSION}.txt"
ls -lh "${ROOT}/${OUT}/SHA256SUMS_v${VERSION}.txt" "$ZIP"
