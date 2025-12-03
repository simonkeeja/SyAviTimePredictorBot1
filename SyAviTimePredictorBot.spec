# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Projects\\SyAviTimePredictorBot\\attached_assets\\SyAviTimePredictorBot_1764276181880.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Projects\\SyAviTimePredictorBot\\attached_assets\\SyAviBackgroundPic.jpeg', '.'), ('C:\\Projects\\SyAviTimePredictorBot\\attached_assets\\SyAviTimePredictorIcon_3D.png', '.')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='SyAviTimePredictorBot',
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
    icon=['C:\\Projects\\SyAviTimePredictorBot\\attached_assets\\SyAviBackgroundPic.jpeg'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SyAviTimePredictorBot',
)
