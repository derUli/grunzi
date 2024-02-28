import time
import uuid

import PIL
import arcade
from arcade import get_four_byte_color

MARGIN = 10
class InventoryItem(arcade.sprite.Sprite):

    def __init__(self, filename, bottom, left):

        super().__init__(filename=filename)
        self.bottom = bottom
        self.left = left

        self.original_texture = PIL.Image.open(filename).convert('RGBA')

        self.selected = False
        self.name = time.time()

        self.names = [
            uuid.uuid4().hex,
            uuid.uuid4().hex
        ]

    def setup(self, i, selected=False):
        self.update_sprite(selected)
    def select(self):
        self.update_sprite(True)

    def unselect(self):
        self.update_sprite(False)

    def update_sprite(self, selected=False):
        self.selected = selected

        color = arcade.csscolor.BLACK
        if self.selected:
            color = arcade.csscolor.DARK_GREY

        name = self.names[int(self.selected)]
        image = PIL.Image.new("RGBA", self.original_texture.size, get_four_byte_color(color))

        image.paste(self.original_texture, (0,0), self.original_texture)

        texture = arcade.texture.Texture(name=name, image=image)

        self.texture = texture
