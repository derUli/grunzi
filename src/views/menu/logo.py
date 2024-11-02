""" Main menu """
import os

import arcade.gui

from views.fading import Fading

class Logo(Fading):
    """ Main menu """

    def __init__(self, window, state, player=None):
        """
        Constructor
        @param window: arcade.Window
        @param state: SettingsState
        """
        super().__init__(window)

        self.window = window
        self.state = state
        self.manager = arcade.gui.UIManager(window)
        self.scene = arcade.Scene()

    def on_show_view(self) -> None:
        """ On show view """
        arcade.set_background_color(arcade.color.WHITE)

        self.state.settings.unmute()
        self.window.set_mouse_visible(False)

        logo = arcade.Sprite(filename=os.path.join(self.state.ui_dir, 'hog-games.png'), center_x = 0, center_y = 0)
        logo.center_x = self.window.width / 2
        logo.center_y = self.window.height / 2
        self.scene.add_sprite('logo', logo)

    def on_hide_view(self) -> None:
        """ On hide view """

        self.window.set_mouse_visible(True)


    def on_update(self, delta_time: float) -> None:
        """ on update """

        super().on_update(delta_time=delta_time)

        self.update_fade()


    def on_draw(self) -> None:
        """ on draw """

        self.clear()

        self.camera_gui.use()
        self.scene.draw()

        self.draw_fading()
        self.draw_after()
