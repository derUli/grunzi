import os
import time

import arcade.gui

from views.gameview import GameView


class MenuView(arcade.View):
    """Main menu view class."""

    def __init__(self, window, state, main_view = None):
        super().__init__()

        self.window = window
        self.manager = arcade.gui.UIManager()

        self.state = state

        v_box = arcade.gui.UIBoxLayout()

        newgame_button = arcade.gui.UIFlatButton(text="New Game", width=150)

        quit_button = arcade.gui.UIFlatButton(text="Quit game", width=150)

        self.player = None

        @newgame_button.event("on_click")
        def on_click_newgame_button(event):
            start_time = time.time()
            # Pass already created view because we are resuming.
            view = GameView(self.window, self.state)

            print(time.time() - start_time)
            self.window.show_view(view)

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            arcade.close_window()

        buttons = [
            newgame_button,
            quit_button
        ]

        for button in buttons:
            v_box.add(button.with_space_around(bottom=20))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=v_box)
            )

        self.state = state

        self.main_view = main_view

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()
        self.player.pause()

    def on_show_view(self):
        """ This is run once when we switch to this view """

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])

        music = arcade.load_sound(os.path.join(self.state.music_dir, 'menu.ogg'))
        self.player = music.play(loop=True)

        self.manager.enable()

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()
        self.manager.draw()