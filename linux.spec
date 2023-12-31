# -*- mode: python ; coding: utf-8 -*-

from kivymd import hooks_path as kivymd_hooks_path

block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("./backend/*.py", "backend"),
        ("./ui/accountselectscreen/*.*", "ui/accountselectscreen"),
        ("./ui/assets/*.png", "ui/assets"),
        ("./ui/components/*.py", "ui/components"),
        ("./ui/components/message_components/*.py", "ui/components/message_components"),
        ("./ui/messagescreen/*.*", "ui/messagescreen"),
        ("./ui/welcomescreen/*.*", "ui/welcomescreen"),
        ("./ui/progressscreen/*.*", "ui/progressscreen"), 
        ],
    hiddenimports=[],
    hookspath=[kivymd_hooks_path],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

splash = Splash(
    "ui/assets/Splash Screen.png",
    binaries=a.binaries,
    datas=a.datas,
)


pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    splash,
    splash.binaries,
    a.binaries,
    a.datas,
    name='MR.DM',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="ui/assets/icon.png"
)