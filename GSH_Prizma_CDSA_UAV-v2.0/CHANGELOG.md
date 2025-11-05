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

## v1.2.5 — 2025-11-02 20:24:06 (Europe/Berlin)

### Added
- Система подсказок/помощи: `assets/help/help_ru.json` + подключение в GUI.
- Восстановлен и расширен список «Местность»: Городская, Пригород, Село/Дерев, Равнинная, Лес, Холмистая, Горная, Море/Водоём, Река/Долина.
- Унифицированный маппинг `ENV_MAP_RU2KEY` в `calc.py` для ветвления моделей.
- Вычисление чувствительности приёмника (kTB + NF + SNRmin), заготовка для LoRa (`lora_required_snr_db`).
- Builder‑kit: скрипты `pack_deb.sh` и `pack_rpm.sh` на базе **fpm**; `gsh_prizma_gui.spec` для **PyInstaller**; `make_zip.sh`; `version_tag.sh`.
- Пример проекта: `examples/sample_project.gshprizma`.
- Запускной скрипт: `scripts/run_dev_verbose.sh`.

### Changed
- Нормализация единиц измерения: внутренняя СИ, на UI МГц/км/дБм; формат поля «Полоса, МГц» — `#####.###`.
- Валидации диапазонов (скелет): h_TX/h_RX → 0.1–12000 м; частоты 100–6000 МГц.
- UX: «Сохранить/Открыть» закрепляются кнопками внизу (реализация будет на уровне таба в основном проекте).

### Fixed
- Подготовлен шаблон устранения проблемы `unindent`/смешанных отступов (реальная правка будет в файле `tab_link.py` основного проекта).
- Починены настройки оси X (логарифм/формат без степеней) — зафиксировано на уровне дизайна (реальная правка относится к UI кода проекта).

---

## v1.2.4 — 2025-11-01 (контекст)
- Базовая рабочая версия перед развилкой на 1.2.5. Записи по 1.2.4 собраны в ветках Gen1/Gen2/Gen3 (см. историю).


## v1.2.4r1 — 2025-11-02 19:51:33
 - README: добавлен верхний баннер с «замороженной» SHA256 и краткими командами запуска/сборки.
 - README: добавлена секция **Checksums**.
 - GUI/Plot: режимы масштаба переведены на радиокнопки; соответствие: Простой → semilogX, Логарифмический → linear, Полулогарифмический → log–log.
 - UI: выравнены ширины комбобоксов «Модем», «Антенна TX», «Антенна RX»; прочие поля приведены к единой ширине.
 - Packaging: builder‑kit (Makefile, scripts/*), fpm-скрипты для .deb/.rpm, PyInstaller one-folder для Windows.
 - CLI: `gsh_prizma/cli.py` и `ui/app.py` — единая точка входа.
 - Лаунчер: `run_dev_verbose.sh` — запуск проекта из корня.

## FPM arg-array fix v1.2.5
 - Распаковать поверх:
   unzip -o builder-kit-fpm-arrayfix-v1.2.5.zip -d ~/work/GSH_Prizma-v1.2.5/
   chmod +x ~/work/GSH_Prizma-v1.2.5/builder-kit/*.sh
 - Пересобрать пакеты:
   MODE=pyinstaller bash builder-kit/pack_deb.sh
   sudo apt install -y rpm   # если нужно
   MODE=pyinstaller bash builder-kit/pack_rpm.sh

## Builder-kit fix v1.2.5
 - Распаковать в корень проекта:
   unzip builder-kit-fix-v1.2.5.zip -d ~/work/GSH_Prizma-v1.2.5/
   chmod +x ~/work/GSH_Prizma-v1.2.5/builder-kit/*.sh
 - Быстрый смоук:
   cd ~/work/GSH_Prizma-v1.2.5
   bash builder-kit/smoke_test.sh
 - Отдельно пакеты:
   MODE=pyinstaller bash builder-kit/pack_deb.sh
   MODE=pyinstaller bash builder-kit/pack_rpm.sh
## Тонкости:
 - Скрипты сами создадут локальный venv builder-kit/.pyi-venv при отсутствии активного .venv (PEP 668-safe).
 - fpm ставится через gem (sudo потребуется), для rpm-пакета на Debian нужен apt install rpm.
 - PyInstaller: выход допускает one-file (dist/gsh-prizma-gen3) и one-folder (dist/gsh-prizma-gen3/gsh-prizma-gen3).
