# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from kivy_deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, hookspath, runtime_hooks

block_cipher = None

directorio_raiz = os.path.abspath(".")
directorio_src = os.path.join(directorio_raiz, "src")

# Recopilar dependencias mínimas de Kivy
kivy_deps_dict = get_deps_minimal(video=None, audio=None)

a = Analysis(
    [os.path.join(directorio_src, "view", "gui", "pension_gui.py")],
    pathex=[directorio_src, directorio_raiz],
    binaries=kivy_deps_dict.get("binaries", []),
    datas=[
        (os.path.join(directorio_raiz, "doc"), "doc"),
    ],
    hiddenimports=kivy_deps_dict.get("hiddenimports", []) + [
        "model.logica_pension",
        "dataclasses",
        "csv",
        "datetime",
    ],
    hookspath=hookspath(),
    hooksconfig={},
    runtime_hooks=runtime_hooks(),
    excludes=kivy_deps_dict.get("excludes", []) + [
        "tkinter",
        "_tkinter",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="CalculadoraPensional",
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

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    strip=False,
    upx=True,
    upx_exclude=[],
    name="CalculadoraPensional",
)
