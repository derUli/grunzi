import os
import time

import arcade.cache
from PIL import ImageOps
from arcade import Texture

from sprites.characters.character import Character
from utils.spritesheetanimation import SpriteSheetReader


class CharacterAnimation:

    cache: dict = {}

    def __init__(self):
        self._textures = []
        self._last_update = 0
        self._frame_length = 0
        self._current_frame_index = 0
        self._loop = True
        self._apply_modifier = True

    def load(self, size, state, filename, loop, frame_length, apply_modifier, resize, character, autocrop=False):
        self._last_update = time.time()
        self._loop = loop
        self._frame_length = frame_length

        self._apply_modifier = apply_modifier
        self._textures = []

        if filename in CharacterAnimation.cache:
            self._textures = CharacterAnimation.cache[filename]
            return

        reader = SpriteSheetReader(os.path.join(state.sprite_dir, 'char', character, filename))
        reader.process(size=size, resize=resize, autocrop=autocrop, pil_resample=state.settings.pil_resample)

        i = 0
        for image in reader.images:
            self._textures.append([
                Texture('img_' + str(filename) + '_' + str(i) + '_right', image=image),
                Texture('img_' + str(filename) + '_' + str(i) + '_left', image=ImageOps.mirror(image))
            ])

            i += 1

        CharacterAnimation.cache[filename] = self._textures


    def update(self, modifier=1) -> bool:

        modifier = modifier - 1

        if not self._apply_modifier:
            modifier = 0

        modified_frame_duration = self._frame_length - (self._frame_length * modifier)

        new_value = self._current_frame_index + 1

        if time.time() - self._last_update >= modified_frame_duration:

            if new_value >= len(self._textures):
                if self._loop:
                    self._current_frame_index = 0
                else:
                    self._current_frame_index = self._current_frame_index
            else:
                self._current_frame_index = new_value
                self._last_update = time.time()
            return True

        return False

    @property
    def current_frame(self):
        return self._textures[self._current_frame_index]

    @property
    def loop(self):
        return self._loop

    @property
    def last_frame(self):
        return self._current_frame_index >= len(self._textures) - 1

    @property
    def completed(self):
        return not self.loop and self.last_frame

    def reset(self):
        self._last_update = time.time()
        self._current_frame_index = 0
