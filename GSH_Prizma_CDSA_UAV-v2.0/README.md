# GSH Prizma Gen3 CDSA UAV — v1.2.4r1
**SHA256 (frozen, external file next to the archive)**: WILL_BE_FILLED
**Напоминание по запуску:**
```bash
unzip GSH_Prizma_Gen3_CDSA_UAV-v1.2.4r1-all.zip
cd GSH_Prizma_Gen3_CDSA_UAV-v1.2.4r1
./run_dev_verbose.sh
```

**Сборка (кратко):**
```bash
make check
make wheel
make deb
make rpm
make exe
```

## Checksums
Каноническая сумма — во внешнем файле `*.SHA256` рядом с архивом. Проверка:
```bash
sha256sum -c GSH_Prizma_Gen3_CDSA_UAV-v1.2.4r1-all.SHA256
```

# GSH_Prizma_Gen3_CDSA_UAV

**Release:** v1.2.1  
**Date/Time:** 2025-11-01 00:13:25 CET  
**SHA256:** см. `SHA256SUMS.txt` (текущий релиз сверху).

## Кратко
Единый инструмент (Gen3) на Python + PySide6:
- **Antenna Wizard Lite** — стартовые размеры и экспорт `.nec/.json` (штырь 1/4λ, патч, мини-яги (3 эл.), компактная спираль);
- **Линк-бюджет/Дальность** — L_max, инверсия Hata/COST-231 в d_link, радиогоризонт, теоретическая дальность = min(d_link, d_horizon).

## Быстрый старт (установка колеса)
```bash
unzip GSH_Prizma_Gen3_CDSA_UAV-v1.2.1-src.zip
cd GSH_Prizma_Gen3_CDSA_UAV-v1.2.0-src

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install build
python -m build
python -m pip install dist/*.whl

prizma-cdsa gui
```

## Изменения (новое — сверху)
- 2025-11-01 00:13:25 CET — v1.2.0: переход на **Gen3**, фиксы GUI (устойчивый backend Matplotlib qtagg→qt5agg), починен отступ в `tab_link.py`, добален `run_dev.sh`, обновлён `BUILD.md` (канонический путь), структура релиза приведена к правилам (unzip/cd в начале).


## Запуск из зафиксированного пути (~/work/run_dev_verbose.sh)

Если вы используете персональный скрипт запуска, расположенный по фиксированному пути:
`~/work/run_dev_verbose.sh`, рекомендованный способ таков:
```bash
cd ~/work/GSH_Prizma_Gen3_CDSA_UAV-v1.2.0-src
cp ~/work/run_dev_verbose.sh ./
chmod +x ./run_dev_verbose.sh
./run_dev_verbose.sh
```

Альтернативно можно добавить алиас в `~/.bashrc`:
```bash
echo "alias prizma-dev='cd ~/work/GSH_Prizma_Gen3_CDSA_UAV-v1.2.0-src && ./run_dev_verbose.sh'" >> ~/.bashrc
source ~/.bashrc
prizma-dev
```


### Новое в v1.2.3
- Гарантированный запуск GUI
- Кнопки отчёта над кнопками проекта; уменьшена ширина

