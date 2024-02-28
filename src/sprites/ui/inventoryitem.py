import uuid

import PIL
import arcade
from arcade import get_four_byte_color

MARGIN = 10
PADDING = 5


class InventoryItem(arcade.sprite.Sprite):

    def __init__(self, filename, bottom, left):
        super().__init__(filename=filename)
        self.bottom = bottom
        self.left = left

        self.image = PIL.Image.open(filename).convert('RGBA')

        self.selected = False

        self.names = None

        self.item = None

    def setup(self, i, selected=False, item=None):
        self.set_item(item)
        self.update_sprite(selected)

    def set_item(self, item):
        self.item = item
        self.generate_cache_names()
        self.update_sprite(self.selected)

    def generate_cache_names(self):
        self.names = [
            uuid.uuid4().hex,
            uuid.uuid4().hex
        ]

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
        image = PIL.Image.new("RGBA", self.image.size, get_four_byte_color(color))

        image.paste(self.image, (0, 0), self.image)

        width = self.width - PADDING
        height = self.height - PADDING


        if self.item:
            scaled_item = PIL.ImageOps.fit(self.item.image, (width, height))
            x, y = int(self.width / 2), int(self.height / 2)

            x -= int(scaled_item.width / 2)
            y -= int(scaled_item.height / 2)

            image.paste(scaled_item, (x, y), scaled_item)

        texture = arcade.texture.Texture(name=name, image=image)

        self.texture = texture
