import os

import arcade.gui

import utils
from sprites.backdrops.scrollingbackdrop import ScrollingBackdrop
from utils.text import get_style
from views.fadingview import FadingView
from views.mainmenuview import MainMenuView

BUTTON_WIDTH = 250


class PauseMenuView(FadingView):
    """Main menu view class."""

    def __init__(self, window, state, previous_view=None):
        super().__init__(window)

        self.window = window
        self.manager = arcade.gui.UIManager(window)

        self.state = state

        v_box = arcade.gui.UIBoxLayout()

        newgame_button = arcade.gui.UIFlatButton(text=_("Continue"), width=BUTTON_WIDTH, style=get_style())
        quit_button = arcade.gui.UIFlatButton(text=_("Back to main menu"), width=BUTTON_WIDTH, style=get_style())

        self.backdrop = ScrollingBackdrop(
            filename=os.path.join(
                self.state.image_dir,
                'backdrops',
                'menu.jpg'
            ),
        )

        self.backdrop.width = self.window.width
        self.backdrop.height = self.window.height

        self.scene.add_sprite('backdrop', self.backdrop)

        # A non-scrolling camera that can be used to draw GUI elements

        self.previous_view = previous_view

        @newgame_button.event("on_click")
        def on_click_newgame_button(event):
            # Pass already created view because we are resuming.
            self.window.show_view(self.previous_view)

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            self.next_view = MainMenuView(self.window, self.state)
            self.fade_out()

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

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        super().on_show_view()

        self.camera_gui.move_to(
            (
                self.backdrop.center_x - (self.camera_gui.viewport_width / 2),
                self.backdrop.center_y - (self.camera_gui.viewport_height / 2)
            )
        )

        self.manager.enable()

    def on_update(self, dt):
        self.update_fade(self.next_view)
        self.scene.update()

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()
        self.camera_gui.use()

        self.scene.draw()
        self.manager.draw()

        build_version = os.path.join(self.state.root_dir, 'VERSION.txt')
        utils.text.draw_build_number(build_version, self.window)

        if self.next_view:
            self.draw_fading()
