#!/usr/bin/env python3

""" cx_freeze setup file """
import sys
import cx_Freeze

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

target = cx_Freeze.Executable(
    script="grunzi.py",
    icon='icon.ico',
    base=base,

    target_name='Grunzi.exe'
)

options = {
        'build_exe': {
            # "include_msvcr": True, Not allowed to legal reasons
            'packages': [
                'pygame',
                'sprites',
                'PygameShader'
            ],
            'optimize': 0,
            'include_files': [
                'data/',
                '../CREDITS.txt',
                '../README.txt',
                '../CHANGES.txt',
                '../VERSION'
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
