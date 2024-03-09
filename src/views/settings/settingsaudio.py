""" Settings > Audio """
import arcade.gui

import constants.controls.keyboard
import utils.text
from utils.gui import get_texture_by_value
from views.fading import Fading

BUTTON_WIDTH = 250


class SettingsAudio(Fading):
    """ Settings > Audio """

    def __init__(self, window, state, previous_view, shadertoy, time=0):
        super().__init__(window)

        self.window = window
        self.state = state
        self.manager = arcade.gui.UIManager(window)
        self.shadertoy = shadertoy
        self.time = time

        self.previous_view = previous_view
        self._fade_in = None

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.pop_controller_handlers()
        self.manager.disable()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        super().on_show_view()

        self.push_controller_handlers()
        self.window.set_mouse_visible(True)

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])

        self.setup()

    def setup(self):
        self.manager.clear()
        self.manager.disable()

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            style=utils.text.get_style()
        )

        music_button = arcade.gui.UITextureButton(
            text=_("Music"),
            width=BUTTON_WIDTH,
            texture=get_texture_by_value(
                width=BUTTON_WIDTH,
                height=back_button.height,
                value=self.state.settings._music_volume > 0.0
            ),
            style=utils.text.get_style()
        )

        sound_button = arcade.gui.UITextureButton(
            text=_("Sound"),
            width=BUTTON_WIDTH,
            texture=get_texture_by_value(
                width=BUTTON_WIDTH,
                height=back_button.height,
                value=self.state.settings._sound_volume > 0.0
            ),
            style=utils.text.get_style()
        )

        @back_button.event("on_click")
        def on_click_back_button(event):
            # Pass already created view because we are resuming.
            self.on_back()

        @music_button.event("on_click")
        def on_click_music_button(event):
            # Pass already created view because we are resuming.
            self.on_toggle_music()

        @sound_button.event("on_click")
        def on_click_sound_button(event):
            # Pass already created view because we are resuming.
            self.on_toggle_sound()

        widgets = [
            back_button,
            music_button,
            sound_button
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

    def on_back(self) -> None:
        """ Back button clicked """
        self.previous_view.time = self.time
        self.window.show_view(self.previous_view)

    def on_toggle_music(self):
        """ Toggle music """
        if self.state.settings._music_volume > 0.0:
            self.state.settings._music_volume = 0.0
        else:
            self.state.settings._music_volume = 1.0

        # We can't import this at the beginning of the
        # file because it would be a circular import
        from views.mainmenu import MainMenu

        # Main Menu or game
        main_menu = self.previous_view.previous_view

        # Update volume of main menu music
        if isinstance(main_menu, MainMenu):
            main_menu.player.volume = self.state.settings._music_volume

        self.state.settings.save()

        # Update button color
        self.setup()

    def on_toggle_sound(self) -> None:
        """
        Toggle sound effect
        """
        if self.state.settings._sound_volume > 0.0:
            self.state.settings._sound_volume = 0.0
        else:
            self.state.settings._sound_volume = 1.0

        self.state.settings.save()
        self.setup()
