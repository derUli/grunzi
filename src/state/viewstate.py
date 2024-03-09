import glob
import logging
import os
import random

import arcade
import pyglet
from arcade.experimental import Shadertoy

from constants.maps import FIRST_MAP
from utils.audio import normalize_volume


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
        self._music_volume = 1
        self._sound_volume = 1

        self.shaders = {}
        self.sounds = {}

        self.map_name = map_name
        self.map_name_first = map_name
        self._muted = False

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
                streaming=False
            ),
            'screenshot': arcade.load_sound(
                os.path.join(self.sound_dir, 'common', 'screenshot.ogg'),
                streaming=False
            ),
            'beep': arcade.load_sound(
                os.path.join(self.sound_dir, 'common', 'beep.ogg'),
                streaming=False
            ),
            'shot': arcade.load_sound(
                os.path.join(self.sound_dir, 'weapons', 'shot.ogg'),
                streaming=False
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
            }
        }

        dir = os.path.join(self.sound_dir, 'atmos', '*.ogg')
        for file in glob.glob(dir):
            path = file
            name = os.path.splitext(os.path.basename(path))[0]

            self.sounds['atmos'][name] = arcade.load_sound(path)

        for i in range(1, 6):
            self.sounds[f"grunt{i}"] = arcade.load_sound(
                os.path.join(self.sound_dir, 'pig', f"grunt{i}.ogg"),
                streaming=False
            )

        for i in range(1, 6):
            self.sounds[f"squeak{i}"] = arcade.load_sound(
                os.path.join(self.sound_dir, 'pig', f"squeak{i}.ogg"),
                streaming=False
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

        return sound.play(volume=self.sound_volume, loop=loop)

    def grunt(self):
        rand = random.randint(1, 5)
        logging.info('Grunt')
        return self.play_sound(f"grunt{rand}")

    def squeak(self):
        rand = random.randint(1, 5)
        logging.info('Squeak')
        return self.play_sound(f"squeak{rand}")

    def is_silent(self):
        return pyglet.options['audio'] == 'silent'

    def beep(self):
        return self.play_sound('beep')

    def mute(self):
        self._muted = True

    def unmute(self):
        self._muted = False


    @property
    def music_volume(self):
        if self.is_silent() or self._muted:
            return 0.0

        return self._music_volume

    @music_volume.setter
    def music_volume(self, volume):
        volume = normalize_volume(volume)

        self._music_volume = volume

    @property
    def sound_volume(self):
        if self.is_silent() or self._muted:
            return 0.0

        return self._sound_volume

    @sound_volume.setter
    def sound_volume(self, volume):
        if volume < 0:
            volume = 0.0

        if volume > 1:
            volume = 1.0

        volume = round(volume, 2)
        logging.info('Audio: New volume %s', volume)
        self._sound_volume = volume
