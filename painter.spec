# -*- mode: python ; coding: utf-8 -*-

import sys
import shutil
import glob
import os

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

block_cipher = None

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Compile application executable
a = Analysis(
    ['main.py'],
    pathex=['K:\\dev\\DarksideRP\\AtlasPreviewTool'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Painter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Compile data directory
if not os.path.exists('{0}/config'.format(DISTPATH)):
    shutil.copytree('assets/config', '{0}/config'.format(DISTPATH))

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Copy Panda3d DLLs to output directory
import panda3d
p3d_module = os.path.dirname(panda3d.__file__)
p3d_sdk = os.path.join(p3d_module, "..")
abs_p3d_sdk = os.path.abspath(p3d_sdk)

bin_folder = os.path.join(abs_p3d_sdk, 'bin')
files = glob.iglob(os.path.join(bin_folder, '*.dll'))
for dll in files:
    if os.path.isfile(dll) and not os.path.exists('{0}/{1}'.format(DISTPATH, dll)):
        shutil.copy2(dll, DISTPATH)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#