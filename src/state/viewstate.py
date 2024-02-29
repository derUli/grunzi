import logging
import os
import random

import arcade
import pyglet
from arcade.experimental import Shadertoy


class ViewState:
    def __init__(self, root_dir, map_name='world'):
        self.root_dir = root_dir
        self.data_dir = os.path.join(root_dir, 'data')
        self.map_dir = os.path.join(self.data_dir, 'levels')
        self.image_dir = os.path.join(self.data_dir, 'images')
        self.sprite_dir = os.path.join(self.image_dir, 'sprites')
        self.music_dir = os.path.join(self.data_dir, 'music')
        self.sound_dir = os.path.join(self.data_dir, 'sounds')
        self.font_dir = os.path.join(self.data_dir, 'fonts')
        self.shader_dir = os.path.join(self.data_dir, 'shaders')
        self.music_volume = 1
        self.sound_volume = 1

        self.shaders = {}
        self.sounds = {}

        self.map_name = map_name

    def preload(self):
        self.preload_sounds()
        self.preload_fonts()

        self.shaders = {}

    def preload_fonts(self):
        arcade.load_font(os.path.join(self.font_dir, 'laila.ttf'))
        arcade.load_font(os.path.join(self.font_dir, 'adrip1.ttf'))
        arcade.load_font(os.path.join(self.font_dir, 'consolasmonobook.ttf'))

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
            )
        }

        for i in range(1, 6):
            self.sounds[f"grunt{i}"] = arcade.load_sound(
                os.path.join(self.sound_dir, 'pig', f"grunt{i}.ogg"),
                streaming=False
            )

    def load_shader(self, size, name):

        path = os.path.join(self.shader_dir, name + '.glsl')

        if name in self.shaders:
            return self.shaders[name]

        with open(path, 'r') as f:
            code = f.read()
        self.shaders[name] = Shadertoy(size, code)

        return self.shaders[name]

    def play_sound(self, name):
        return self.sounds[name].play(volume=self.sound_volume)

    def grunt(self):
        rand = random.randint(1, 5)
        logging.debug(_('Grunt'))
        return self.play_sound(f"grunt{rand}")

    def is_silent(self):
        return pyglet.options['audio'] == 'silent'
