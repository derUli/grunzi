import os
import time

from PIL import ImageOps
from arcade import Texture

from utils.spritesheetanimation import SpriteSheetReader


class CharacterAnimation:
    def __init__(self):
        self._textures = []
        self._last_update = 0
        self._frame_length = 0
        self._current_frame_index = 0
        self._loop = True

    def load(self, size, state, filename, loop, frame_length):
        self._last_update = time.time()
        self._loop = loop
        self._frame_length = frame_length

        reader = SpriteSheetReader(os.path.join(state.sprite_dir, 'char', 'pig', filename))
        reader.process(size=size, resize=(63, 35), autocrop=False)

        self._textures = []

        i = 0
        for image in reader.images:
            self._textures.append([
                Texture('img_' + str(filename) + '_' + str(i) + '_right', image=image),
                Texture('img_' + str(filename) + '_' + str(i) + '_left', image=ImageOps.mirror(image))
            ])

            i += 1

    def update(self, modifier=1) -> bool:
        modifier = modifier - 1
        modified_frame_duration= self._frame_length - (self._frame_length * modifier)

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
    def completed(self):
        return not self.loop and self._current_frame_index >= len(self._textures) - 1


    def reset(self):
        self._last_update = time.time()
        self._current_frame_index = 0