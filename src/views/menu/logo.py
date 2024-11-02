""" Main menu """
import os

import arcade.gui
import pyglet.clock

from views.fading import Fading
from views.menu.mainmenu import MainMenu


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
        self.sound = None
        self.transition = False

    def on_show_view(self) -> None:

        """ On show view """

        # TODO: Add options to skip logo as argument and hidden setting

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

        self.update_fade(self.next_view)

        if self.transition:
            return

        if self._fade_in is None and not self.sound:
            self.sound = self.state.grunt()
            self.sound.volume = self.state.settings.sound_volume

        if self.sound and not self.sound.playing:
            self.transition = True
            pyglet.clock.schedule_once(self.fade_to_mainmenu, 3)


    def on_draw(self) -> None:
        """ on draw """

        self.clear()

        self.camera_gui.use()
        self.scene.draw()

        self.draw_fading()
        self.draw_after()

    def fade_to_mainmenu(self, dt) -> None:
        self.fade_to_view(MainMenu(self.window, self.state))