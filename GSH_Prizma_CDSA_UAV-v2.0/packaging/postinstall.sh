#!/usr/bin/env bash
set -euo pipefail
APPDIR="/opt/gsh_prizma_cdsauav-__VER__"
VENV="$APPDIR/.venv"

command -v python3 >/dev/null
python3 -m venv "$VENV"
"$VENV/bin/pip" install --upgrade pip
# локальная установка колеса и зависимостей
if ls "$APPDIR/dist/"gsh_prizma_cdsauav-*.whl >/dev/null 2>&1; then
  "$VENV/bin/pip" install PySide6 matplotlib "$APPDIR"/dist/gsh_prizma_cdsauav-*.whl
else
  # fallback: из исходников
  "$VENV/bin/pip" install PySide6 matplotlib "$APPDIR"
fi

# лаунчер
cat > /usr/bin/prizma-cdsa <<'EOF'
#!/usr/bin/env bash
APPDIR="/opt/gsh_prizma_cdsauav-__VER__"
VENV="$APPDIR/.venv"
exec "$VENV/bin/python" -m gsh_prizma.cli "$@"
EOF
chmod +x /usr/bin/prizma-cdsa
echo "[postinstall] Installed prizma-cdsa launcher."
