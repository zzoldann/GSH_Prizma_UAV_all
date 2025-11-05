# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

ROOT = os.path.abspath(os.getcwd())
MAIN = os.path.join(ROOT, 'src', 'gsh_prizma', '__main__.py')
pathex = [ROOT, os.path.join(ROOT, 'src')]
hiddenimports = collect_submodules('PySide6')
datas = [(os.path.join(ROOT, 'assets', 'help', 'help_ru.json'), 'assets/help')]

a = Analysis([MAIN], pathex=pathex, binaries=[], datas=datas,
             hiddenimports=hiddenimports, hookspath=[], hooksconfig={},
             runtime_hooks=[], excludes=[], noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts, a.binaries, a.zipfiles, a.datas,
          name='gsh-prizma-gen3', console=False)
