#!/usr/bin/env python3

""" cx_freeze setup file """
import os
import sys

import cx_Freeze

target_name = 'grunzi'
ffmpeg_file = None
base = None

if sys.platform == 'win32':
    target_name = 'Grunzi.exe'
    base = "Win32GUI"
    ffmpeg_file = 'ffmpeg.exe'

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

if ffmpeg_file:
    options['build_exe']['include_files'].append(ffmpeg_file)

cx_Freeze.setup(
    name='Grunzi',
    options=options,
    executables=[
        target
    ]
)
