import logging

import arcade.gui
from arcade.gui import UISlider

import constants.controls.keyboard
import utils.gui
import utils.text
from utils.media.video import video_supported
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
        self.background = COLOR_BACKGROUND

        self.filmgrain_slider = None
        self.antialiasing_slider = None
        self.weather_button = None
        self.colortint_button = None

        self.needs_restart = False

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

    def on_back(self) -> None:
        if not self.needs_restart:
            return self._on_back()

        message_box = arcade.gui.UIMessageBox(
            width=300,
            height=200,
            message_text=_('You may have to restart the game to apply the changed graphics settings.'),
            buttons=[
                _("OK")
            ]
        )

        @message_box.event('on_action')
        def on_back(event):
            logging.debug(event)
            self._on_back()

        self.manager.add(message_box)

    def _on_back(self):
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

        quality_label = arcade.gui.UILabel(
            text=_('Quality'),
            text_color=arcade.csscolor.BLACK,
            bold=True,
            font_name=utils.text.FONT_DEFAULT,
            font_size=utils.text.FONT_SIZE_MEDIUM,
            width=BUTTON_WIDTH,
            align='center'
        )

        quality_slider = UISlider(
            width=BUTTON_WIDTH,
            value=int(self.state.settings.quality),
            min_value=0,
            max_value=6,
            style=utils.gui.get_slider_style()
        )

        @quality_slider.event("on_change")
        def on_change_quality(event):
            self.on_change_quality(event.new_value)

        antialiasing_label = arcade.gui.UILabel(
            text=_('Antialiasing'),
            text_color=arcade.csscolor.BLACK,
            bold=True,
            font_name=utils.text.FONT_DEFAULT,
            font_size=utils.text.FONT_SIZE_MEDIUM,
            width=BUTTON_WIDTH,
            align='center'
        )

        self.antialiasing_slider = UISlider(
            width=BUTTON_WIDTH,
            value=int(self.state.settings.antialiasing),
            min_value=0,
            max_value=16,
            style=utils.gui.get_slider_style()
        )

        @self.antialiasing_slider.event("on_change")
        def on_change_antialiasing(event):
            self.on_change_antialiasing(event.new_value)

        filmgrain_label = arcade.gui.UILabel(
            text=_('Film Grain'),
            text_color=arcade.csscolor.BLACK,
            bold=True,
            font_name=utils.text.FONT_DEFAULT,
            font_size=utils.text.FONT_SIZE_MEDIUM,
            width=BUTTON_WIDTH,
            align='center'
        )

        self.filmgrain_slider = UISlider(
            width=BUTTON_WIDTH,
            value=float(self.state.settings.filmgrain),
            min_value=0,
            max_value=1,
            style=utils.gui.get_slider_style()
        )

        @self.filmgrain_slider.event("on_change")
        def on_change_filmgrain(event):
            self.on_change_filmgrain(event.new_value)

        self.weather_button = arcade.gui.UITextureButton(
            text=_("Weather"),
            width=BUTTON_WIDTH,
            texture=utils.gui.get_texture_by_value(
                width=BUTTON_WIDTH,
                height=back_button.height,
                value=self.state.settings.weather
            ),
            style=utils.gui.get_button_style()
        )

        @self.weather_button.event("on_click")
        def on_change_weather(event):
            self.on_change_weather()

        self.colortint_button = arcade.gui.UITextureButton(
            text=_("Color Tint"),
            width=BUTTON_WIDTH,
            texture=utils.gui.get_texture_by_value(
                width=BUTTON_WIDTH,
                height=back_button.height,
                value=self.state.settings.color_tint
            ),
            style=utils.gui.get_button_style()
        )

        @self.colortint_button.event("on_click")
        def on_change_colortint(event):
            self.on_change_colortint()

        videos_button = arcade.gui.UITextureButton(
            text=_("Videos"),
            width=BUTTON_WIDTH,
            texture=utils.gui.get_texture_by_value(
                width=BUTTON_WIDTH,
                height=back_button.height,
                value=self.state.settings.videos
            ),
            style=utils.gui.get_button_style()
        )

        @videos_button.event("on_click")
        def on_change_videos(event):
            self.on_change_videos()

        @back_button.event("on_click")
        def on_click_back_button(event):
            logging.debug(event)
            self.on_back()

        widgets = [
            back_button,
            quality_label,
            quality_slider,
            antialiasing_label,
            self.antialiasing_slider,
            filmgrain_label,
            self.filmgrain_slider,
            self.weather_button,
            self.colortint_button
        ]

        if video_supported():
            widgets += [videos_button]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=20, align='center')

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

    def on_change_quality(self, quality: float) -> None:

        # Workaround for visual issue
        self.manager._do_render(force=True)

        quality = int(quality)

        if quality != self.state.settings.quality:
            self.state.settings.quality = quality
            self.state.settings.save()
            self.needs_restart = True

            self.filmgrain_slider.value = self.state.settings.filmgrain
            self.antialiasing_slider.value = self.state.settings.antialiasing

            fog_texture = utils.gui.get_texture_by_value(
                width=BUTTON_WIDTH,
                height=self.weather_button.height,
                value=self.state.settings.weather)
            self.weather_button.texture = fog_texture

            colortint_texture = utils.gui.get_texture_by_value(
                width=BUTTON_WIDTH,
                height=self.weather_button.height,
                value=self.state.settings.color_tint)
            self.colortint_button.texture = colortint_texture

    def on_change_filmgrain(self, intensity: float) -> None:

        self.manager._do_render(force=True)
        self.state.settings.filmgrain = intensity
        self.state.settings.save()

    def on_change_antialiasing(self, val: float):
        self.manager._do_render(force=True)

        self.state.settings.antialiasing = val

        self.state.settings.save()
        self.needs_restart = True

    def on_change_weather(self):
        from views.menu.mainmenu import MainMenu
        self.needs_restart = isinstance(self.previous_view.previous_view, MainMenu)
        self.state.settings.weather = not self.state.settings.weather
        self.state.settings.save()
        self.setup()

    def on_change_colortint(self):
        from views.menu.mainmenu import MainMenu
        self.needs_restart = isinstance(self.previous_view.previous_view, MainMenu)

        self.state.settings.color_tint = not self.state.settings.color_tint
        self.state.settings.save()
        self.setup()

    def on_change_videos(self):
        self.state.settings.videos = not self.state.settings.videos
        self.state.settings.save()
        self.setup()
