# GSH Prizma Gen3 CDSA UAV — v1.2.5 (source-only)

**SHA256 (заморозка релиза): см. файл `SHA256SUMS_v1.2.5.txt` в корне архива.**

## Изменения (сверху последние)
- Полный список — см. `CHANGELOG.md` (записи добавляются **выше** старых).

## Быстрый старт (из исходников)
```bash
unzip GSH_Prizma_Gen3_CDSA_UAV-v1.2.5-src.zip
cd GSH_Prizma_Gen3_CDSA_UAV-v1.2.5-src

python3 -m venv .venv && source .venv/bin/activate
pip install -r builder-kit/requirements.txt

# Запуск GUI (скелет):
export PYTHONPATH="$PWD/src"
python -m gsh_prizma

# Сборка бинарника (PyInstaller) и .deb/.rpm через fpm:
pyinstaller --noconfirm builder-kit/gsh_prizma_gui.spec
MODE=pyinstaller bash builder-kit/pack_deb.sh
MODE=pyinstaller bash builder-kit/pack_rpm.sh
```

## Стандарты релиза
- Только исходники + примеры.
- SHA256 — отдельный файл `SHA256SUMS_v1.2.5.txt` (текущая версия — **вверху**).
- В `CHANGELOG.md` новые записи — **выше** старых.
- Инструкции всегда начинаются с `unzip ...` затем `cd ...`.
