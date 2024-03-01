import PIL
import arcade

SCALE = 0.6


class Coin(arcade.sprite.Sprite):
    def __init__(self, filename, center_x, center_y):
        self.filename = filename

        self.image = PIL.Image.open(filename).convert('RGBA').crop()

        texture = arcade.texture.Texture(name='coin', image=self.image)
        super().__init__(
            texture=texture,
            center_x=center_x,
            center_y=center_y,
            scale=SCALE
        )
