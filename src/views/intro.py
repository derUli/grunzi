import os

import arcade.gui

from views.fading import Fading
from views.mainmenu import MainMenu

SPRITE_LIST_ENEMIES = 'ui'

# Seconds
WAIT_FOR = 3


class Intro(Fading):
    """Main menu view class."""

    def __init__(self, window, state):
        super().__init__(window)

        self.state = state
        fps_second = 1000 / 1000 / self.window.draw_rate

        self.wait_for = fps_second * WAIT_FOR
        self.wait_since = 0

    def on_show_view(self):
        """ This is run once when we switch to this view """
        super().on_show_view()

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.csscolor.WHITE])

        logo = arcade.sprite.Sprite(
            filename=os.path.join(
                self.state.image_dir,
                'ui',
                'logo.png'
            ),
            center_x=self.window.width / 2,
            center_y=self.window.height / 2,
        )

        self.scene.add_sprite(SPRITE_LIST_ENEMIES, logo)

    def on_update(self, dt):
        self.scene.update()
        self.update_fade(self.next_view)

    def on_draw(self):
        """ Render the screen. """

        if self._fade_in is None and self._fade_out is None:
            if self.wait_since <= 0:
                self.state.grunt()

            self.wait_since += 1

        if self.wait_since > self.wait_for and not self.next_view:
            self.next_view = MainMenu(self.window, self.state)
            self.fade_out()

        # Clear the screen
        self.clear()

        self.camera_gui.use()

        self.scene.draw()
        self.draw_fading()
        self.draw_debug()
