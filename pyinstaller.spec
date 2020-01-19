# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
	['main.py'],
    pathex=['word-jam'],
    binaries=[],
    datas=[
    	('src/wordjam.kv', 'src/wordjam.kv'),
    	('res/', 'res/'),
    	('lvl/', 'lvl/'),
	],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(
	a.pure,
	a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
	pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Word Jam',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=True,
	icon='res/icon.ico'
)

coll = COLLECT(
	exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=True,
    upx=True,
    upx_exclude=[],
    name='main'
)
