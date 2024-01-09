# -*- mode: python ; coding: utf-8 -*-

from kivymd import hooks_path as kivymd_hooks_path
from kivy_deps import sdl2, glew

block_cipher = None


a = Analysis(
    ['./src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("./src/backend/*.py", "backend"),
        ("./src/ui/accountselectscreen/*.*", "ui\\accountselectscreen"),
        ("./src/ui/assets/*.png", "ui\\assets"),
        ("./src/ui/components/*.py", "ui\\components"),
        ("./src/ui/components/message_components/*.py", "ui\\components\\message_components"),
        ("./src/ui/messagescreen/*.*", "ui\\messagescreen"),
        ("./src/ui/welcomescreen/*.*", "ui\\welcomescreen"),
        ("./src/ui/progressscreen/*.*", "ui\\progressscreen"), 
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
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
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
