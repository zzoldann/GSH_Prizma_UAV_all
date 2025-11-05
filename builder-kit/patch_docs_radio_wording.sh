#!/usr/bin/env bash
set -euo pipefail
V="1.2.5"
CH="CHANGELOG.md"
if [[ -f "$CH" ]]; then
  sed -i '0,/чекбоксы/s//радиокнопки/' "$CH"
  sed -i '0,/«Без степени по X»/s//«Линейная (без 1eN)»/' "$CH"
  echo "[docs] Wording adjusted to radio-buttons for v$V"
fi
