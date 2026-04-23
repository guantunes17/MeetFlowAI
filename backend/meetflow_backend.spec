# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for the MeetFlow AI FastAPI backend sidecar.
# Build with: pyinstaller meetflow_backend.spec  (inside backend/ with venv active)

import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ["run.py"],
    pathex=[str(Path(".").resolve())],
    binaries=[],
    datas=[
        # Ship the default SQLite db path placeholder (app creates it on first run)
    ],
    hiddenimports=[
        "uvicorn.logging",
        "uvicorn.loops",
        "uvicorn.loops.auto",
        "uvicorn.protocols",
        "uvicorn.protocols.http",
        "uvicorn.protocols.http.auto",
        "uvicorn.protocols.websockets",
        "uvicorn.protocols.websockets.auto",
        "uvicorn.lifespan",
        "uvicorn.lifespan.on",
        "passlib.handlers.pbkdf2",
        "passlib.handlers.bcrypt",
        "sqlalchemy.dialects.sqlite",
        "sqlalchemy.sql.default_comparator",
        "spellchecker",
        "email_validator",
        "docx",
        "reportlab",
        "reportlab.lib.pagesizes",
        "reportlab.pdfgen",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=["whisper", "torch", "torchaudio"],
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
    name="meetflow-backend",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,       # sem janela de terminal no Windows
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
