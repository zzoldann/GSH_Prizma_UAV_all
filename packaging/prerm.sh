#!/usr/bin/env bash
set -euo pipefail
APPDIR="/opt/gsh_prizma_cdsauav-__VER__"
rm -f /usr/bin/prizma-cdsa || true
# не трогаем APPDIR (на случай пользовательских файлов); при purge пользователь может удалить вручную
exit 0
