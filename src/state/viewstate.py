import glob
import logging
import os
import random

import arcade
import pyglet
from arcade.experimental import Shadertoy

from constants.maps import FIRST_MAP
from utils.audio import streaming_enabled


class ViewState:
    def __init__(self, root_dir, map_name=FIRST_MAP, settings=None):
        self.root_dir = root_dir
        self.data_dir = os.path.join(root_dir, 'data')
        self.map_dir = os.path.join(self.data_dir, 'maps')
        self.image_dir = os.path.join(self.data_dir, 'images')
        self.sprite_dir = os.path.join(self.image_dir, 'sprites')
        self.music_dir = os.path.join(self.data_dir, 'music')
        self.sound_dir = os.path.join(self.data_dir, 'sounds')
        self.font_dir = os.path.join(self.data_dir, 'fonts')
        self.shader_dir = os.path.join(self.data_dir, 'shaders')
        self.video_dir = os.path.join(self.data_dir, 'videos')

        self.shaders = {}
        self.sounds = {}

        self.map_name = map_name
        self.map_name_first = map_name
        self.difficulty = None

        self.settings = settings

    def preload(self):
        self.preload_sounds()
        self.preload_fonts()

        self.shaders = {}

    def preload_fonts(self):
        pyglet.font.add_directory(self.font_dir)

    def preload_sounds(self):
        self.sounds = {
            'coin': arcade.load_sound(
                os.path.join(self.sound_dir, 'common', 'pickup.ogg'),
            ),
            'screenshot': arcade.load_sound(
                os.path.join(self.sound_dir, 'common', 'screenshot.ogg'),
            ),
            'beep': arcade.load_sound(
                os.path.join(self.sound_dir, 'common', 'beep.ogg'),
            ),
            'shot': arcade.load_sound(
                os.path.join(self.sound_dir, 'weapons', 'shot.ogg'),
            ),
            'screech': arcade.load_sound(
                os.path.join(self.sound_dir, 'skull', 'screech.ogg'),
            ),
            'atmos': {
            },
            'piggybank': {
                'destroy': arcade.load_sound(os.path.join(self.sound_dir, 'piggybank', 'destroy.ogg'))
            },
            'tools': {
                'plier': arcade.load_sound(os.path.join(self.sound_dir, 'plier', 'plier.ogg'))
            },
            'car': {
                'start': arcade.load_sound(os.path.join(self.sound_dir, 'car', 'car_start.ogg'))
            }
        }

        dir = os.path.join(self.sound_dir, 'atmos', '*.ogg')

        for file in glob.glob(dir):
            path = file
            name = os.path.splitext(os.path.basename(path))[0]
            self.sounds['atmos'][name] = arcade.load_sound(path)

        for i in range(1, 6):
            self.sounds[f"grunt{i}"] = arcade.load_sound(
                os.path.join(self.sound_dir, 'pig', f"grunt{i}.ogg")
            )

        for i in range(1, 6):
            self.sounds[f"squeak{i}"] = arcade.load_sound(
                os.path.join(self.sound_dir, 'pig', f"squeak{i}.ogg")
            )

    def load_shader(self, size, name):

        path = os.path.join(self.shader_dir, name + '.glsl')

        if name in self.shaders:
            return self.shaders[name]

        if not os.path.exists(path):
            return None

        with open(path, 'r') as f:
            code = f.read()
        self.shaders[name] = Shadertoy(size, code)

        return self.shaders[name]

    def play_sound(self, name1, name2=None, loop=False):
        try:
            sound = self.sounds[name1]
            if name2:
                sound = sound[name2]
        except KeyError:
            return

        return sound.play(volume=self.settings.sound_volume, loop=loop)

    def grunt(self):
        rand = random.randint(1, 5)
        logging.info('Grunt')
        return self.play_sound(f"grunt{rand}")

    def squeak(self):
        rand = random.randint(1, 5)
        logging.info('Squeak')
        return self.play_sound(f"squeak{rand}")

    def beep(self):
        return self.play_sound('beep')
