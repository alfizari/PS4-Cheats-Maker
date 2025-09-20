# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
import sys

datas = []
binaries = []
hiddenimports = []
tmp_ret = collect_all('lupa')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,        # Needed for macOS app bundles
    target_arch=None,           # PyInstaller auto-detects (x86 on 32-bit Python, x86_64 on 64-bit)
    codesign_identity=None,     # Set if you need macOS signing
    entitlements_file=None,
    icon=['logo/logo.icns'] if sys.platform == "darwin" else ['logo\\logo.ico'],
)

