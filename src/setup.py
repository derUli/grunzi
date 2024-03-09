#!/usr/bin/env python3

""" cx_freeze setup file """
import os
import sys
import shutil

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
        'optimize': 0,
        'includes': [
            'PyAudio'
        ],
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

# If Linux delete the video related stuff because it won't work on Linux
if sys.platform != 'win32':
    os.unlink('build/exe.linux-x86_64-3.10/data/3rdparty/ffmpeg.exe')
    shutil.rmtree('build/exe.linux-x86_64-3.10/data/videos')
