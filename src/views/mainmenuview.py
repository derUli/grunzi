import os

import arcade.gui

import utils.text
from sprites.backdrops.scrollingbackdrop import ScrollingBackdrop
from views.fadingview import FadingView


class MainMenuView(FadingView):
    """Main menu view class."""

    def __init__(self, window, state):
        super().__init__(window)

        self.window = window
        self.manager = arcade.gui.UIManager(window)

        self.state = state

        v_box = arcade.gui.UIBoxLayout()

        newgame_button = arcade.gui.UIFlatButton(text=_("New Game"), width=200)

        quit_button = arcade.gui.UIFlatButton(text=_("Quit game"), width=200)
        self.player = None

        self.scene = arcade.Scene()

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

        self.next_view = None
        # A non-scrolling camera that can be used to draw GUI elements

        @newgame_button.event("on_click")
        def on_click_newgame_button(event):
            # Pass already created view because we are resuming.

            self.fade_out()
            from views.gameview import GameView
            self.next_view = GameView(self.window, self.state)

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            self.fade_quit()

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

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()
        self.player.pause()

    def on_show_view(self):
        super().on_show_view()
        """ This is run once when we switch to this view """

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])

        music = arcade.load_sound(os.path.join(self.state.music_dir, 'menu.ogg'))
        self.player = music.play(loop=True)

        self.camera_gui = arcade.Camera()

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

        self.scene.draw()
        self.manager.draw()

        build_version = os.path.join(self.state.root_dir, 'VERSION')
        utils.text.draw_build_number(build_version, self.window)
        self.draw_fading()
        self.camera_gui.use()
