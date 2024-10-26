import os
import time

from PIL import ImageOps
from arcade import Texture

from utils.spritesheetanimation import SpriteSheetReader


class CharacterAnimation:
    def __init__(self):
        self.textures = []
        self.last_update = 0
        self.frame_duration = 0.1
        self.current_frame_index = 0

    def load(self, size, state, filename):
        self.last_update = time.time()
        reader = SpriteSheetReader(os.path.join(state.sprite_dir, 'char', 'pig', filename))
        reader.process(size=size, resize=(63, 35), autocrop=False)

        self.textures = []

        i = 0
        for image in reader.images:
            self.textures.append([
                Texture('img_' + str(filename) + '_' + str(i) + '_right', image=image),
                Texture('img_' + str(filename) + '_' + str(i) + '_left', image=ImageOps.mirror(image))
            ])

            i += 1

    def update(self, modifier=1) -> bool:
        modifier = modifier - 1
        modified_frame_duration = self.frame_duration - (self.frame_duration * modifier)

        if time.time() - self.last_update >= modified_frame_duration:
            self.current_frame_index += 1
            if self.current_frame_index >= len(self.textures):
                self.current_frame_index = 0

            self.last_update = time.time()
            return True

        return False

    @property
    def current_frame(self):
        return self.textures[self.current_frame_index]
