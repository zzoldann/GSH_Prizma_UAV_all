# BUILD

## 0) Разархивирование и переход в каталог
```bash
unzip GSH_Prizma_Gen3_CDSA_UAV-v1.2.5-src.zip
cd GSH_Prizma_Gen3_CDSA_UAV-v1.2.5-src
```

## 1) Локальный запуск из исходников
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r builder-kit/requirements.txt
export PYTHONPATH="$PWD/src"
python -m gsh_prizma
```

## 2) Сборка бинарника (PyInstaller)
```bash
pyinstaller --noconfirm builder-kit/gsh_prizma_gui.spec
./dist/gsh-prizma-gen3/gsh-prizma-gen3
```

## 3) Сборка пакетов .deb/.rpm через fpm
Требуется Ruby и fpm (`sudo gem install fpm`), либо скрипты сами установят.

### .deb
```bash
MODE=pyinstaller bash builder-kit/pack_deb.sh
ls -lh *.deb
```

### .rpm
```bash
MODE=pyinstaller bash builder-kit/pack_rpm.sh
ls -lh *.rpm
```

## 4) Архив исходников и SHA256
```bash
bash builder-kit/make_zip.sh
cat SHA256SUMS_v1.2.5.txt
```
