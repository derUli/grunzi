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

cx_Freeze.setup(
    name='Grunzi',
    options={
        'build_exe': {
            'packages': [
                'pygame',
                'sprites',
                'PygameShader'
            ],
            'include_files': [
                'data/',
                '../CREDITS.txt',
                '../README.txt',
                '../CHANGES.txt',
                '../VERSION'
            ]
        }
    },
    executables=[
        target
    ]
)
