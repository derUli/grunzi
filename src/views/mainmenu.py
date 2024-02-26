import os

import arcade.gui

import utils.text
from views.fading import Fading
from views.optionsmenu import OptionsMenu

BUTTON_WIDTH = 250


class MainMenu(Fading):
    """Main menu view class."""

    def __init__(self, window, state):
        super().__init__(window)

        self.window = window
        self.state = state

        self.manager = arcade.gui.UIManager(window)

        v_box = arcade.gui.UIBoxLayout()

        label = arcade.gui.UILabel(
            text=_('Grunzi'),
            font_name=utils.text.ADRIP_FONT,
            font_size=utils.text.LOGO_FONT_SIZE,
            text_color=arcade.csscolor.HOTPINK,
            align='center'
        )

        newgame_button = arcade.gui.UIFlatButton(
            text=_("New Game"),
            width=BUTTON_WIDTH,
            stye=utils.text.get_style()
        )

        options_help = arcade.gui.UIFlatButton(
            text=_("Options & Help"),
            width=BUTTON_WIDTH,
            stye=utils.text.get_style()
        )

        quit_button = arcade.gui.UIFlatButton(
            text=_("Quit game"),
            width=BUTTON_WIDTH,
            style=utils.text.get_style()
        )

        self.player = None

        size = self.window.width, self.window.height
        self.shadertoy = self.state.load_shader(size, 'pigs')

        self.time = 0

        @newgame_button.event("on_click")
        def on_click_newgame_button(event):
            # Pass already created view because we are resuming.

            from views.game import Game
            self.next_view = Game(self.window, self.state)
            self.state.reset()
            self.fade_out()

        @options_help.event("on_click")
        def on_click_options_help(event):
            # Pass already created view because we are resuming.

            self.window.show_view(
                OptionsMenu(self.window, self.state, previous_view=self, shadertoy=self.shadertoy, time=self.time)
            )

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            self.fade_quit()

        buttons = [
            label,
            newgame_button,
            options_help,
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

        if self.next_view:
            self.player.pause()

    def on_show_view(self):
        super().on_show_view()
        """ This is run once when we switch to this view """

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])

        music = arcade.load_sound(os.path.join(self.state.music_dir, 'menu.ogg'))

        if not self.player:
            self.player = music.play(loop=True)

        self.manager.enable()

    def on_update(self, dt):
        self.time += dt
        self.update_fade(self.next_view)
        self.scene.update()

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()
        self.camera_gui.use()

        arcade.start_render()
        self.shadertoy.render(time=self.time)

        self.manager.draw()
        self.draw_build_version()

        self.draw_fading()
