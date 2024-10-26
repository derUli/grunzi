import os
import time

from PIL import ImageOps
from arcade import Texture

from utils.spritesheetanimation import SpriteSheetReader


class WalkingAnimation:
    def __init__(self):
        self.textures = []
        self.last_update = 0
        self.frame_duration = 0.010
        self.current_frame_index = 0

    def load(self, state):
        self.last_update = time.time()
        reader = SpriteSheetReader(os.path.join(state.sprite_dir, 'char', 'pig', 'pig_walk_run.png'))
        reader.process(size=(360, 194), resize=(63, 35))

        self.textures = []

        i = 0
        for image in reader.images:
            self.textures.append([
                Texture('img_' + str(i) + '_right', image=image),
                Texture('img_' + str(i) + '_left', image=ImageOps.mirror(image))
            ])

            i += 1


    def update(self):
        if time.time() - self.last_update > self.frame_duration:
            self.current_frame_index += 1
            if self.current_frame_index >= len(self.textures):
                self.current_frame_index = 0

            self.last_update = time.time()
            return True

        return False


    @property
    def current_frame(self):
        return self.textures[self.current_frame_index]

