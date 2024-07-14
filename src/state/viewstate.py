import glob
import logging
import os
import random
from typing import Tuple

import arcade
import pyglet
from arcade.experimental import Shadertoy
from pyglet import media

from constants.maps import FIRST_MAP
from utils.keypressed import KeyPressed


class ViewState:
    def __init__(self, root_dir: str, map_name=FIRST_MAP, settings=None):
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
        self.animation_dir = os.path.join(self.data_dir, 'animations')
        self.shaders = {}
        self.sounds = {}

        self.map_name = map_name
        self.map_name_first = map_name
        self.difficulty = None
        self._score = 0
        self.settings = settings
        self.keypressed = KeyPressed()

    def reset(self) -> None:
        """ Reset ViewState """

        self._score = 0
        self.keypressed.reset()

    def preload(self) -> None:
        """ Preload stuff """

        self.preload_sounds()
        self.preload_fonts()
        self.shaders = {}

    def preload_fonts(self) -> None:
        """ Preload all fonts """
        pyglet.font.add_directory(self.font_dir)

    def preload_sounds(self) -> None:
        """ Preload sounds """
        self.sounds = {
            'coin': arcade.load_sound(
                os.path.join(self.sound_dir, 'common', 'pickup.ogg'),
            ),
            'screenshot': arcade.load_sound(
                os.path.join(self.sound_dir, 'common', 'screenshot.ogg'),
            ),
            'noaction': arcade.load_sound(
                os.path.join(self.sound_dir, 'pig', 'noaction.ogg'),
            ),
            'shot': arcade.load_sound(
                os.path.join(self.sound_dir, 'weapons', 'shot.ogg'),
            ),
            'screech': arcade.load_sound(
                os.path.join(self.sound_dir, 'skull', 'screech.ogg'),
            ),
            'slimer': arcade.load_sound(
                os.path.join(self.sound_dir, 'slimer', 'slimer.ogg'),
            ),
            'footsteps': arcade.load_sound(
                os.path.join(self.sound_dir, 'pig', 'footsteps.ogg')
            ),
            'smacks': arcade.load_sound(os.path.join(self.sound_dir, 'pig', 'smacks.ogg')),
            'piggybank': {
                'destroy': arcade.load_sound(os.path.join(self.sound_dir, 'piggybank', 'destroy.ogg'))
            },
            'tools': {
                'plier': arcade.load_sound(os.path.join(self.sound_dir, 'plier', 'plier.ogg'))
            },
            'car': {
                'start': arcade.load_sound(os.path.join(self.sound_dir, 'car', 'car_start.ogg'))
            },
            'electric': {
                'on': arcade.load_sound(os.path.join(self.sound_dir, 'electric', 'on.ogg')),
                'push': arcade.load_sound(os.path.join(self.sound_dir, 'electric', 'push.ogg'))
            },
            'cactus': arcade.load_sound(os.path.join(self.sound_dir, 'cactus', 'cactus.ogg')),
            'valve': arcade.load_sound(os.path.join(self.sound_dir, 'valve', 'valve.ogg')),
            'loading': arcade.load_sound(os.path.join(self.music_dir, 'loading.ogg')),
            'atmos': {},
            'explosion': arcade.load_sound(os.path.join(self.sound_dir, 'weapons', 'explosion.ogg'))
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

    def load_shader(self, size: Tuple[int, int], name: str) -> Shadertoy|None:

        path = os.path.join(self.shader_dir, name + '.glsl')

        if name in self.shaders:
            return self.shaders[name]

        if not os.path.exists(path):
            return None

        with open(path, 'r') as f:
            code = f.read()

        self.shaders[name] = Shadertoy(size, code)

        return self.shaders[name]

    def play_sound(
            self,
            name1: str,
            name2: str | None = None,
            loop: bool = False,
            speed: float = 1,
            volume: float = 1
    ) -> media.Player:
        try:
            sound = self.sounds[name1]
            if name2:
                sound = sound[name2]
        except KeyError as e:
            logging.error(e)
            return

        return sound.play(volume=volume * self.settings.sound_volume, loop=loop, speed=speed)

    def grunt(self) -> media.Player:
        """ play random grunt sound """
        rand = random.randint(1, 5)
        logging.info('Grunt')
        return self.play_sound(f"grunt{rand}")

    def squeak(self) -> media.Player:
        rand = random.randint(1, 5)
        logging.info('Squeak')
        return self.play_sound(f"squeak{rand}")

    def noaction(self) -> media.Player:
        return self.play_sound('noaction')

    @property
    def score(self) -> int:
        return self._score

    @score.setter
    def score(self, val: int) -> None:
        last_digit = int(str(val)[-1])

        if last_digit >= 5:
            last_digit = 5
        else:
            last_digit = 0

        val = int(str(val)[:-1] + str(last_digit))

        self._score = val
