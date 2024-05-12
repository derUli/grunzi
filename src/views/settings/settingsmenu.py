import arcade.gui

import constants.controls.keyboard
import utils.gui
import utils.text
from views.fading import Fading
from views.settings.settingsaudio import SettingsAudio
from views.settings.settingscontrols import SettingsControls
from views.settings.video.settingsdisplay import SettingsDisplay
from views.settings.video.settingsgraphics import SettingsGraphics

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

    def on_show_view(self):
        """ This is run once when we switch to this view """
        super().on_show_view()

        self.push_controller_handlers()
        self.window.set_mouse_visible(True)

        self.setup()

    def on_hide_view(self):
        super().on_hide_view()
        # Disable the UIManager when the view is hidden.
        self.pop_controller_handlers()
        self.manager.disable()

    def on_back(self):
        self.previous_view.time = self.time
        self.window.show_view(self.previous_view)

    def setup(self):
        self.manager.clear()
        self.manager.disable()

        # Video settings
        button_display = arcade.gui.UIFlatButton(
            text=_("Display"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        # Video settings
        button_graphics = arcade.gui.UIFlatButton(
            text=_("Graphics"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        # Video settings
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
            comeback_view = SettingsMenu(self.window, self.state, self.previous_view, self.shadertoy, 0)

            # Pass already created view because we are resuming.
            self.next_view = SettingsControls(self.window, self.state, comeback_view)
            self.fade_out()

        @button_display.event("on_click")
        def on_click_display_button(event):
            self.window.show_view(
                SettingsDisplay(
                    self.window,
                    self.state,
                    previous_view=self,
                    shadertoy=self.shadertoy,
                    time=self.time
                ),
            )

        @button_graphics.event("on_click")
        def on_click_graphics_button(event):
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
            # Pass already created view because we are resuming.
            self.on_back()

        widgets = [
            back_button,
            button_display
        ]

        # Check if this is running from pause menu
        from views.pausemenu import PauseMenu
        game_running = isinstance(self.previous_view, PauseMenu)

        if not game_running:
            widgets += [button_graphics]

        if not self.state.settings.is_silent():
            widgets += [audio_button]

        widgets += [
            controls_button
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=10, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout())
        frame.with_padding(bottom=20)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.manager.enable()

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)

        """Called whenever a key is pressed."""
        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_back()

    def on_update(self, delta_time):

        super().on_update(delta_time)

        self.update_mouse()
        self.update_fade(self.next_view)
        self.scene.update()

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()
        self.camera_gui.use()
        self.render_shadertoy()

        self.manager.draw()
        self.draw_build_version()

        self.draw_fading()
        self.draw_debug()

    def on_toggle_fps(self):
        super().on_toggle_fps()
        self.setup()

    def on_toggle_fullscreen(self):
        super().on_toggle_fullscreen()
        self.setup()
