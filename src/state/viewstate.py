import logging
import os
import random

import arcade


class ViewState:
    def __init__(self, root_dir, map_name):
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
        self.map_name = map_name

    def preload(self):
        self.preload_sounds()
        self.preload_fonts()

    def preload_fonts(self):
        arcade.load_font(os.path.join(self.fonts_dir, 'laila.ttf'))
        arcade.load_font(os.path.join(self.fonts_dir, 'adrip1.ttf'))
        arcade.load_font(os.path.join(self.fonts_dir, 'consolasmonobook.ttf'))

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
            'shot': arcade.load_sound(
                os.path.join(self.sound_dir, 'weapons', 'shot.ogg'),
                streaming=False
            )
        }

        for i in range(1, 6):
            self.sounds[f"grunt{i}"] = arcade.load_sound(
                os.path.join(self.sound_dir, 'pig', f"grunt{i}.ogg"),
                streaming=False
            )

    def play_sound(self, name):
        return self.sounds[name].play()

    def grunt(self):
        rand = random.randint(1, 5)
        logging.debug(_('Grunt'))
        return self.play_sound(f"grunt{rand}")

