import os

import PIL
import arcade.gui

from sprites.sprite import Sprite
from views.fading import Fading
from views.menu.mainmenu import MainMenu

LAYER_UI = 'ui'

# Seconds
WAIT_FOR = 3

MARGIN = 10

COLOR_BACKGROUND = [rgb - 50 for rgb in arcade.csscolor.WHITE]


class Intro(Fading):
    """Main menu view class."""

    def __init__(self, window, state):
        """ Constructor """
        super().__init__(window)

        self.state = state

        self.wait_for = 1
        self.wait_since = 0
        self.background = COLOR_BACKGROUND

    def on_show_view(self) -> None:
        """ On show view """
        super().on_show_view()
        self.window.set_mouse_visible(False)

        image = PIL.Image.open(
            os.path.join(self.state.ui_dir, 'logo.png')
        ).convert('RGBA').crop()

        if image.size > self.window.size:
            w, h = self.window.size

            w -= MARGIN * 2
            h -= MARGIN * 2
            image = PIL.ImageOps.pad(image, (w, h))

        texture = arcade.texture.Texture(name='logo', image=image)

        logo = Sprite(
            texture=texture,
            center_x=self.window.width / 2,
            center_y=self.window.height / 2,
        )

        self.scene.add_sprite(LAYER_UI, logo)

    def on_update(self, delta_time: float) -> None:
        """
        On update
        @param delta_time: Delta Time
        """
        super().on_update(delta_time=delta_time)

        self.update_fade(self.next_view)

        if self._fade_in is None and self._fade_out is None:
            if self.wait_since <= 0:
                self.state.grunt()

            self.wait_since += 1

        if self.wait_since > self.wait_for and not self.next_view:
            self.fade_to_view(MainMenu(self.window, self.state))

    def on_draw(self) -> None:
        """ On draw """

        # Clear the screen
        self.clear()
        self.camera_gui.use()

        self.scene.draw()
        self.draw_fading()
        self.draw_after()
