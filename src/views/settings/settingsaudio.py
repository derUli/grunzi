""" Settings > Audio """
import arcade.gui
from arcade.gui.widgets.slider import UISlider

import constants.controls.keyboard
import utils.gui
import utils.text
from views.fading import Fading

BUTTON_WIDTH = 250

COLOR_BACKGROUND = (123, 84, 148)


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

        self.background = COLOR_BACKGROUND

    def on_show_view(self):
        """ This is run once when we switch to this view """
        super().on_show_view()

        self.push_controller_handlers()
        self.window.set_mouse_visible(True)

        self.setup()

    def on_hide_view(self):
        """ Disable the UIManager when the view is hidden. """

        super().on_hide_view()
        self.pop_controller_handlers()
        self.manager.disable()

    def setup(self):
        self.manager.clear()
        self.manager.disable()

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        default_style = arcade.gui.UISlider.UIStyle(
            filled_bar=arcade.color.HOT_PINK,
            unfilled_bar=arcade.color.BLACK
        )

        style_dict = {"press": default_style, "normal": default_style, "hover": default_style,
                      "disabled": default_style}

        music_label = arcade.gui.UILabel(
            text=_('Music'),
            text_color=arcade.csscolor.BLACK,
            bold=True,
            font_size=utils.text.MEDIUM_FONT_SIZE,
            width=BUTTON_WIDTH,
            align='center'
        )

        music_slider = UISlider(
            width=BUTTON_WIDTH,
            value=int(self.state.settings._music_volume * 100),
            min_value=0,
            max_value=100,
            style=style_dict
        )

        sound_label = arcade.gui.UILabel(
            text=_('Sound'),
            text_color=arcade.csscolor.BLACK,
            bold=True,
            font_size=utils.text.MEDIUM_FONT_SIZE,
            width=BUTTON_WIDTH,
            align='center'
        )

        sound_slider = UISlider(
            width=BUTTON_WIDTH,
            value=int(self.state.settings._sound_volume * 100),
            min_value=0,
            max_value=100,
            style=style_dict
        )

        @back_button.event("on_click")
        def on_click_back_button(event):
            # Pass already created view because we are resuming.
            self.on_back()

        @music_slider.event('on_change')
        def on_change_music_volume(event):
            # Workaround for visual issue
            self.manager._do_render(force=True)

            volume = event.new_value

            if volume > 0.0:
                volume = volume / 100
            else:
                volume = 0.0

            volume = round(volume, 2)

            self.state.settings._music_volume = volume
            self.previous_view.previous_view.player.volume = volume

            self.state.settings.save()

        @sound_slider.event("on_change")
        def on_change_sound_volume(event):

            # Workaround for visual issue
            self.manager._do_render(force=True)

            volume = event.new_value

            if volume > 0.0:
                volume = volume / 100
            else:
                volume = 0.0

            volume = round(volume, 2)

            self.state.settings._sound_volume = volume
            self.state.settings.save()

        widgets = [
            back_button,
            music_label,
            music_slider,
            sound_label,
            sound_slider
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
        self.draw_fading()
        self.draw_after(draw_version_number=True)

    def on_back(self) -> None:
        """ Back button clicked """
        self.previous_view.time = self.time
        self.window.show_view(self.previous_view)
