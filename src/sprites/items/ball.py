import os.path

import PIL
import arcade


class Ball(arcade.sprite.Sprite):
    def __init__(self, state):
        filename = os.path.join(state.sprite_dir, 'ball.png')

        self.image = PIL.Image.open(filename).convert('RGBA').crop()
        texture = arcade.texture.Texture(name='ball', image=self.image)
        super().__init__(path_or_texture=texture)
