import arcade


MARGIN = 10

class InventoryItem(arcade.sprite.Sprite):

    def __init__(self, filename, bottom, left):

        super().__init__(filename=filename)
        self.bottom = bottom
        self.left = left
        self.original_texture = self.texture

        self.selected = False

    def setup(self, i, selected=False):
        color = arcade.csscolor.BLACK

        self.selected = selected

        if self.selected:
            color = arcade.csscolor.DARK_GREY

        texture = arcade.texture.Texture.create_filled(
            name='inventory' + str(i),
            size=self.original_texture.size,
            color=color
        )
        self.texture = texture
