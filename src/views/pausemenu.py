import os

import arcade.gui

import constants.controls.keyboard
from utils.audio import streaming_enabled
from utils.gui import get_button_style
from views.fading import Fading
from views.mainmenu import MainMenu
from views.settings.settingsmenu import SettingsMenu

BUTTON_WIDTH = 250

COLOR_BACKGROUND = (74, 146, 182)


class PauseMenu(Fading):
    """ Main menu view class."""

    def __init__(self, window, state, previous_view=None):
        super().__init__(window)

        self.window = window
        self.manager = arcade.gui.UIManager(window)
        self.state = state
        self.previous_view = previous_view
        self.background = COLOR_BACKGROUND
        self.player = None

    def setup(self) -> None:
        """ Set up the pause menu """

        continue_button = arcade.gui.UIFlatButton(
            text=_("Continue"),
            width=BUTTON_WIDTH,
            style=get_button_style()
        )

        restart_button = arcade.gui.UIFlatButton(
            text=_("Restart Level"),
            width=BUTTON_WIDTH,
            style=get_button_style()
        )

        settings_button = arcade.gui.UIFlatButton(
            text=_("Settings"),
            width=BUTTON_WIDTH,
            style=get_button_style()
        )

        quit_button = arcade.gui.UIFlatButton(
            text=_("Back to main menu"),
            width=BUTTON_WIDTH,
            style=get_button_style()
        )

        self.shadertoy = self.state.load_shader(self.window.size, 'gloopy')

        @continue_button.event("on_click")
        def on_click_continue_button(event):
            # Pass already created view because we are resuming.
            self.on_continue()

        @restart_button.event("on_click")
        def on_click_restart(event):
            # Pass already created view because we are resuming.
            self.on_restart_level()

        @settings_button.event("on_click")
        def on_click_settings_button(event):
            # Pass already created view because we are resuming.

            self.window.show_view(
                SettingsMenu(
                    self.window,
                    self.state,
                    previous_view=self,
                    shadertoy=self.shadertoy,
                    time=self.time
                ),
            )

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            self.on_exit()

        widgets = [
            continue_button,
            restart_button,
            settings_button,
            quit_button
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=10, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout())
        frame.with_padding(bottom=20)
        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        music = arcade.load_sound(
            os.path.join(self.state.music_dir, 'pause.ogg'),
            streaming=streaming_enabled()
        )

        self.player = music.play(loop=True, volume=self.state.settings.music_volume)

    def on_show_view(self) -> None:
        """ On show view """
        super().on_show_view()

        self.push_controller_handlers()
        self.manager.enable()

    def on_hide_view(self) -> None:
        """ On hide view """

        super().on_hide_view()

        self.pop_controller_handlers()
        self.manager.disable()

    def on_key_press(self, key, modifiers) -> None:
        """ on Key press """
        super().on_key_press(key, modifiers)

        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_continue()

    def on_continue(self) -> None:
        """
        On continue
        """
        self.player.pause()
        self.window.show_view(self.previous_view)

    def on_restart_level(self):

        """
        On restart level
        """
        message_box = arcade.gui.UIMessageBox(
            width=300,
            height=200,
            message_text=_("Restart level?"),
            buttons=[
                _("Yes"),
                _("No")
            ]
        )

        message_box.on_action = self.on_confirm_restart
        self.manager.add(message_box)

    def on_confirm_restart(self, button):
        if button.action == _('No'):
            return

        from views.game import Game
        self.previous_view = None
        self.fade_to_view(Game(self.window, self.state))
        self.player.pause()

    def on_exit(self, confirm=False):
        if not confirm:
            message_box = arcade.gui.UIMessageBox(
                width=300,
                height=200,
                message_text=
                "\n".join(
                    [
                        _("Leave to main menu?"),
                        _("All progress since the begin of this level will be lost.")
                    ]
                ),
                buttons=[
                    _("Yes"),
                    _("No")
                ]
            )

            message_box.on_action = self.on_confirm_exit
            self.manager.add(message_box)
            return

        self.manager.clear()

        self.player.pause()
        self.fade_to_view(MainMenu(self.window, self.state))

    def on_confirm_exit(self, button) -> None:
        """ On confirm exit """

        if button.action == _('Yes'):
            self.player.pause()
            self.on_exit(confirm=True)

    def on_update(self, delta_time: float) -> None:
        super().on_update(delta_time)

        self.update_mouse()
        self.update_fade(self.next_view)
        self.scene.update()

    def on_draw(self) -> None:
        """ Render the screen. """

        # Clear the screen
        self.clear()
        self.camera_gui.use()
        self.render_shadertoy()

        self.manager.draw()

        if self.next_view:
            self.draw_fading()

        self.draw_after(draw_version_number=True)
