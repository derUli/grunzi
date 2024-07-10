import logging

import arcade.gui
from arcade.gui import UISlider

import constants.controls.keyboard
import utils.gui
import utils.text
from utils.gui import get_texture_by_value
from views.fading import Fading

BUTTON_WIDTH = 250
COLOR_BACKGROUND = (123, 84, 148)


class SettingsScreen(Fading):
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
        # Disable the UIManager when the view is hidden.
        super().on_hide_view()
        self.pop_controller_handlers()
        self.manager.disable()

    def on_back(self):
        self.previous_view.time = self.time
        self.window.show_view(self.previous_view)

    def setup(self) -> None:
        self.manager.clear()
        self.manager.disable()

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        fullscreen_button = arcade.gui.UITextureButton(
            text=_("Fullscreen"),
            width=BUTTON_WIDTH,
            texture=get_texture_by_value(
                width=BUTTON_WIDTH,
                height=back_button.height,
                value=self.window.fullscreen
            ),
            style=utils.gui.get_button_style()
        )

        # Video settings
        vsync_button = arcade.gui.UITextureButton(
            text=_("V-Sync"),
            width=BUTTON_WIDTH,
            texture=get_texture_by_value(
                width=BUTTON_WIDTH,
                height=back_button.height,
                value=self.window.vsync
            ),
            style=utils.gui.get_button_style()
        )

        fps_button = arcade.gui.UITextureButton(
            text=_("Show FPS"),
            width=BUTTON_WIDTH,
            texture=get_texture_by_value(
                width=BUTTON_WIDTH,
                height=back_button.height,
                value=self.state.settings.show_fps
            ),
            style=utils.gui.get_button_style()
        )

        @fullscreen_button.event('on_click')
        def on_click_fullscreen_button(event):
            logging.debug(event)

            self.on_toggle_fullscreen()
            self.setup()

        @vsync_button.event('on_click')
        def on_click_vsync_button(event):
            logging.debug(event)

            self.on_toggle_vsync()
            self.setup()

        @fps_button.event('on_click')
        def on_click_fps_button(event):
            logging.debug(event)

            self.on_toggle_fps()
            self.setup()

        @back_button.event("on_click")
        def on_click_back_button(event):
            logging.debug(event)
            self.on_back()

        widgets = [
            back_button
        ]

        # Toggle fullscreen is pointless if the window size equals to the native screen resolution
        if not self.window.is_native:
            widgets += [
                fullscreen_button
            ]

        # Other video settings
        widgets += [
            vsync_button,
            fps_button
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=10, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout())
        frame.with_padding(bottom=20)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.manager.enable()

    def on_key_press(self, key, modifiers) -> None:
        super().on_key_press(key, modifiers)

        """Called whenever a key is pressed."""
        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_back()

    def on_update(self, delta_time) -> None:

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
        """ On toggle show FPS """

        super().on_toggle_fps()
        self.setup()

    def on_toggle_fullscreen(self) -> None:
        """ On toggle fullscreen """

        super().on_toggle_fullscreen()
        self.setup()