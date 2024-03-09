#!/usr/bin/env python3

""" cx_freeze setup file """
import os
import sys

import cx_Freeze

target_name = 'grunzi'
base = None

if sys.platform == 'win32':
    target_name = 'Grunzi.exe'
    base = "Win32GUI"

target = cx_Freeze.Executable(
    script="grunzi.py",
    icon=os.path.join(
        os.path.dirname(__file__),
        'data',
        'images',
        'ui',
        'icon.ico'
    ),
    base=base,
    target_name=target_name
)

options = {
    'build_exe': {
        # "include_msvcr": True, Not allowed to legal reasons
        'optimize': 2,
        'include_files': [
            'data/',
            '../CREDITS.txt',
            '../README.txt',
            '../CHANGES.txt',
            '../VERSION.txt'
        ]
    }
}

cx_Freeze.setup(
    name='Grunzi',
    options=options,
    executables=[
        target
    ]
)

# If windows delete linux ffmpeg executable
if sys.platform != 'win32':
    os.unlink('build/exe.win-amd64-3.11/data/3rdparty/ffmpeg')
