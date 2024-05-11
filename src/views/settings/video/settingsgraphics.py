import arcade.gui

import constants.controls.keyboard
import utils.gui
import utils.text
from utils.gui import get_texture_by_value
from views.fading import Fading

BUTTON_WIDTH = 250
COLOR_BACKGROUND = (123, 84, 148)

class SettingsGraphics(Fading):
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

    def on_show_view(self):
        """ This is run once when we switch to this view """
        super().on_show_view()

        self.push_controller_handlers()
        self.window.set_mouse_visible(True)

        self.setup()

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        super().on_hide_view()
        self.pop_controller_handlers()
        self.manager.disable()


    def on_back(self):
        self.previous_view.time = self.time
        self.window.show_view(self.previous_view)

    def setup(self):
        arcade.set_background_color(COLOR_BACKGROUND)

        self.manager.clear()
        self.manager.disable()

        # Check if this is running from pause menu
        from views.pausemenu import PauseMenu
        game_running = isinstance(self.previous_view.previous_view, PauseMenu)

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        traffic_button = arcade.gui.UITextureButton(
            text=_("Traffic"),
            width=BUTTON_WIDTH,
            texture=get_texture_by_value(
                width=BUTTON_WIDTH,
                height=back_button.height,
                value=self.state.settings.traffic
            ),
            style=utils.gui.get_button_style()
        )

        sky_button = arcade.gui.UITextureButton(
            text=_("Animated Sky"),
            width=BUTTON_WIDTH,
            texture=get_texture_by_value(
                width=BUTTON_WIDTH,
                height=back_button.height,
                value=self.state.settings.sky
            ),
            style=utils.gui.get_button_style()
        )


        @sky_button.event('on_click')
        def on_click_sky_button(event):
            self.on_toggle_sky()
            self.setup()

        @traffic_button.event('on_click')
        def on_click_traffic_button(event):
            self.on_toggle_traffic()
            self.setup()

        @back_button.event("on_click")
        def on_click_back_button(event):
            # Pass already created view because we are resuming.

            self.on_back()

        widgets = [
            back_button
        ]

        if not game_running:
            widgets += [
                traffic_button,
                sky_button
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
        """Called whenever a key is pressed."""

        super().on_key_press(key, modifiers)

        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_back()

    def on_update(self, delta_time):

        super().on_update(delta_time)

        self.time += delta_time

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

    def on_toggle_sky(self) -> None:
        """ On toggle sky """
        self.state.settings.sky = not self.state.settings.sky
        self.state.settings.save()

    def on_toggle_traffic(self) -> None:
        """ On toggle traffic """
        self.state.settings.traffic = not self.state.settings.traffic
        self.state.settings.save()
