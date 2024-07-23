import logging

import arcade.gui

import constants.controls.keyboard
import utils.gui
import utils.text
from views.fading import Fading
from views.settings.settingsaudio import SettingsAudio
from views.settings.settingscontrols import SettingsControls
from views.settings.settingsgraphics import SettingsGraphics
from views.settings.settingsscreen import SettingsScreen

BUTTON_WIDTH = 250

COLOR_BACKGROUND = (123, 84, 148)


class SettingsMenu(Fading):
    """Main menu view class."""

    def __init__(self, window, state, previous_view, shadertoy, time=0):
        super().__init__(window)

        self.window = window
        self.state = state
        self.manager = arcade.gui.UIManager(window)
        self.shadertoy = shadertoy
        self.time = time

        self.previous_view = previous_view
        self._fade_in = None
        self.background = COLOR_BACKGROUND

    def on_show_view(self) -> None:
        """ This is run once when we switch to this view """
        super().on_show_view()

        self.push_controller_handlers()
        self.window.set_mouse_visible(True)

        self.setup()

    def on_hide_view(self) -> None:
        super().on_hide_view()
        # Disable the UIManager when the view is hidden.
        self.pop_controller_handlers()
        self.manager.disable()

    def on_back(self) -> None:
        self.previous_view.time = self.time
        self.window.show_view(self.previous_view)

    def setup(self) -> None:
        self.manager.clear()
        self.manager.disable()

        # Video settings
        button_screen = arcade.gui.UIFlatButton(
            text=_("Screen"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        button_graphics = arcade.gui.UIFlatButton(
            text=_("Graphics"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        # audio settings
        audio_button = arcade.gui.UIFlatButton(
            text=_("Audio"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        # Control settings
        controls_button = arcade.gui.UIFlatButton(
            text=_("Controls"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        @controls_button.event("on_click")
        def on_click_controls_button(event):
            logging.debug(event)

            comeback_view = SettingsMenu(self.window, self.state, self.previous_view, self.shadertoy, 0)

            # Pass already created view because we are resuming.
            self.fade_to_view(SettingsControls(self.window, self.state, comeback_view))

        @button_screen.event("on_click")
        def on_click_screen(event):
            logging.debug(event)

            self.window.show_view(
                SettingsScreen(
                    self.window,
                    self.state,
                    previous_view=self,
                    shadertoy=self.shadertoy,
                    time=self.time
                ),
            )

        @button_graphics.event("on_click")
        def on_click_graphics(event):
            logging.debug(event)

            self.window.show_view(
                SettingsGraphics(
                    self.window,
                    self.state,
                    previous_view=self,
                    shadertoy=self.shadertoy,
                    time=self.time
                ),
            )

        @audio_button.event("on_click")
        def on_click_audio_button(event):
            logging.debug(event)

            self.window.show_view(
                SettingsAudio(
                    self.window,
                    self.state,
                    previous_view=self,
                    shadertoy=self.shadertoy,
                    time=self.time
                )
            )

        @back_button.event("on_click")
        def on_click_back_button(event):
            logging.debug(event)

            # Pass already created view because we are resuming.
            self.on_back()

        widgets = [
            back_button,
            button_screen,
            button_graphics
        ]

        if not self.state.settings.is_silent():
            widgets += [audio_button]

        widgets += [
            controls_button
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=20, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout())
        frame.with_padding(bottom=20)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.manager.enable()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """ Called whenever a key is pressed """

        super().on_key_press(key, modifiers)

        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_back()

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

        self.draw_fading()
        self.draw_after(draw_version_number=True)

    def on_toggle_fps(self) -> None:
        super().on_toggle_fps()
        self.setup()

    def on_toggle_fullscreen(self) -> None:
        super().on_toggle_fullscreen()
        self.setup()
