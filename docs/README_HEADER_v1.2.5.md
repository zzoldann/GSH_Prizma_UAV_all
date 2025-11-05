# GSH Prizma Gen3 CDSA UAV — v1.2.5

## SHA256
(заполните после сборки релизов)
- gsh-prizma-gen3_1.2.5_amd64.deb — `…`
- gsh-prizma-gen3-1.2.5-1.x86_64.rpm — `…`

## Быстрый старт (из исходников)
```bash
unzip GSH_Prizma-v1.2.5-src.zip
cd GSH_Prizma-v1.2.5
python3 -m venv .venv
source .venv/bin/activate
pip install -r builder-kit/requirements.txt
python -m gsh_prizma
```

## Установка пакетов
```bash
sudo apt install ./builder-kit/out/gsh-prizma-gen3_1.2.5_amd64.deb
# или
sudo rpm -i builder-kit/out/gsh-prizma-gen3-1.2.5-1.x86_64.rpm
```
