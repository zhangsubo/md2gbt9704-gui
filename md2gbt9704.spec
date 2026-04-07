# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

datas = []
try:
    datas += collect_data_files('docx')
except:
    pass

hiddenimports = [
    'PySide6',
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'docx',
    'docx.oxml',
    'docx.shared',
    'docx.text',
    'docx.enum',
    'docx.enum.text',
    'docx.enum.style',
    'docx.oxml.text',
    'docx.oxml.table',
    'docx.oxml.shared',
    'markdown',
    'markdown.core',
    'markdown.extensions',
    'PIL',
    'PIL.Image',
    'chardet',
    'lxml',
    'lxml.etree',
]

runtime_hooks = ['docx_runtime_hook.py']

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=runtime_hooks,
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='md2gbt9704',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
