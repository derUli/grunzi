#!/usr/bin/env python3

""" cx_freeze setup file """

import cx_Freeze
import glob
import json
import os
import shutil
import sys
import xmlformatter

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

OPTIMIZE = 0

if sys.platform == 'win32':
    OPTIMIZE = 1

options = {
    'build_exe': {
        # "include_msvcr": True, Not allowed to legal reasons
        'optimize': OPTIMIZE,
        'silent_level': 3,
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

formatter = xmlformatter.Formatter(compress=True, selfclose=True)

# Minify map files
for file in glob.glob('build/*/data/maps/*.tmx'):
    output = formatter.format_file(file)

    with open(file, 'wb') as f:
        f.write(output)

for file in glob.glob('build/*/data/maps/*.json'):
    with open(file, 'r') as f1:
        minified = json.dumps(json.loads(f1.read()))
        f1.close()

        with open(file, 'w') as f2:
            f2.write(minified)

clean_rubbish = [
    glob.glob('build/*/lib/**/examples', recursive=True),
    glob.glob('build/*/lib/**/tests', recursive=True),
    glob.glob('build/*/lib/**/docs', recursive=True),
    glob.glob('build/*/lib/**/doc', recursive=True),
    glob.glob('build/*/lib/arcade/resources/music', recursive=True),
    glob.glob('build/*/lib/arcade/resources/sounds', recursive=True),
    glob.glob('build/*/lib/arcade/resources/tiled_maps', recursive=True),
    glob.glob('build/*/lib/arcade/resources/images', recursive=True),
    glob.glob('build/*/lib/arcade/resources/cache', recursive=True),
    glob.glob('build/*/lib/arcade/resources/assets', recursive=True),
    glob.glob('build/*/lib/arcade/resources/onscreen_controls', recursive=True)
]

for bulk in clean_rubbish:
    for file in bulk:
        if os.path.isdir(file):
            print(f"Deleting {file}")
            shutil.rmtree(file)
        elif os.path.isfile(file):
            print(f"Deleting {file}")
            os.unlink(file)
