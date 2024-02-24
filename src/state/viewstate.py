import os

import arcade
import pyglet

class ViewState:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.data_dir = os.path.join(root_dir, 'data')
        self.map_dir = os.path.join(self.data_dir, 'levels')
        self.image_dir = os.path.join(self.data_dir, 'images')
        self.sprite_dir = os.path.join(self.image_dir, 'sprites')
        self.music_dir = os.path.join(self.data_dir, 'music')
        self.sound_dir = os.path.join(self.data_dir, 'sounds')
        self.fonts_dir = os.path.join(self.data_dir, 'fonts')

        self.sounds = {}

        self.coins = 0

    def preload(self):
        self.preload_sounds()
        self.preload_fonts()

    def preload_fonts(self):
        arcade.load_font(os.path.join(self.fonts_dir, 'laila.ttf'))


    def preload_sounds(self):
        if not 'coin' in self.sounds:
            self.sounds['coin'] = arcade.load_sound(
                os.path.join(self.sound_dir, 'common', 'pickup.ogg'),
                streaming=False
            )

        if not 'screenshot' in self.sounds:
            self.sounds['screenshot'] = arcade.load_sound(
                os.path.join(self.sound_dir, 'common', 'screenshot.ogg'),
                streaming=False
            )

    def play_sound(self, name):
        if name not in self.sounds:
            self.preload_sounds()

        return self.sounds[name].play()
