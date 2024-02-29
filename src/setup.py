#!/usr/bin/env python3

""" cx_freeze setup file """
import os
import sys

import cx_Freeze

base = None

target_name = 'grunzi'

if sys.platform == 'win32':
    target_name = 'Grunzi'

if sys.platform == 'win32':
    base = "Win32GUI"
    target_name += '.exe'

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
