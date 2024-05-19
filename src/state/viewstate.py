import glob
import logging
import os
import random

import arcade
import pyglet
from arcade.experimental import Shadertoy

from constants.maps import FIRST_MAP
from utils.keypressed import KeyPressed


class ViewState:
    def __init__(self, root_dir, map_name=FIRST_MAP, settings=None):
        self.root_dir = root_dir
        self.data_dir = os.path.join(root_dir, 'data')
        self.map_dir = os.path.join(self.data_dir, 'maps')
        self.image_dir = os.path.join(self.data_dir, 'images')
        self.sprite_dir = os.path.join(self.image_dir, 'sprites')
        self.ui_dir = os.path.join(self.image_dir, 'ui')
        self.postprocessing_dir = os.path.join(self.image_dir, 'postprocessing')
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
        self.score = 0
        self.settings = settings
        self.keypressed = KeyPressed()

    def reset(self):
        self.score = 0

    def preload(self):
        self.preload_sounds()
        self.preload_fonts()

        self.shaders = {}

    def preload_fonts(self):
        """ Preload all fonts """
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
            'footsteps': arcade.load_sound(
                os.path.join(self.sound_dir, 'pig', 'footsteps.ogg')
            ),
            'piggybank': {
                'destroy': arcade.load_sound(os.path.join(self.sound_dir, 'piggybank', 'destroy.ogg'))
            },
            'tools': {
                'plier': arcade.load_sound(os.path.join(self.sound_dir, 'plier', 'plier.ogg'))
            },
            'car': {
                'start': arcade.load_sound(os.path.join(self.sound_dir, 'car', 'car_start.ogg'))
            },
            'water': {
                'splash': arcade.load_sound(os.path.join(self.sound_dir, 'water', 'splash.ogg'))
            },
            'electric': {
                'on': arcade.load_sound(os.path.join(self.sound_dir, 'electric', 'on.ogg')),
                'push': arcade.load_sound(os.path.join(self.sound_dir, 'electric', 'push.ogg'))
            },
            'loading':  arcade.load_sound(os.path.join(self.music_dir, 'loading.ogg')),
            'atmos': {}
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

        for i in range(1, 5):
            self.sounds[f"chainsaw{i}"] = arcade.load_sound(
                os.path.join(self.sound_dir, 'chainsaw', f"chainsaw{i}.ogg")
            )

        for i in range(1, 7):
            self.sounds[f"chicken{i}"] = arcade.load_sound(
                os.path.join(self.sound_dir, 'chicken', f"chicken{i}.ogg")
            )

        for i in range(1, 4):
            self.sounds[f"duck{i}"] = arcade.load_sound(
                os.path.join(self.sound_dir, 'duck', f"duck{i}.ogg")
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

    def play_sound(self, name1, name2=None, loop=False, speed=1, volume=1):
        try:
            sound = self.sounds[name1]
            if name2:
                sound = sound[name2]
        except KeyError as e:
            logging.error(e)
            return

        return sound.play(volume=volume * self.settings.sound_volume, loop=loop, speed=speed)

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
