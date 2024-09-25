""" Main menu """

import logging
import os

import arcade.gui

import utils.gui
import utils.text
from constants.fonts import FONT_ADRIP
from utils.media.audio import streaming_enabled
from views.menu.campaignmenu import CampaignMenu
from views.fading import Fading
from views.settings.settingsmenu import SettingsMenu

BUTTON_WIDTH = 250
BUTTON_MARGIN_BOTTOM = 20

COLOR_BACKGROUND = (123, 84, 148)


class MainMenu(Fading):
    """ Main menu """

    def __init__(self, window, state, player = None):
        """
        Constructor
        @param window: arcade.Window
        @param state: SettingsState
        """
        super().__init__(window)

        self.window = window
        self.state = state
        self.manager = arcade.gui.UIManager(window)
        self.background = COLOR_BACKGROUND

        label = arcade.gui.UILabel(
            text=_('Grunzi'),
            font_name=FONT_ADRIP,
            font_size=utils.text.FONT_SIZE_LOGO,
            text_color=arcade.csscolor.HOTPINK,
            align='center',
        )

        campaign_button = arcade.gui.UIFlatButton(
            text=_("Campaign"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        options_button = arcade.gui.UIFlatButton(
            text=_("Settings"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        quit_button = arcade.gui.UIFlatButton(
            text=_("Quit game"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        self.player = None

        size = self.window.size
        self.shadertoy = self.state.load_shader(size, 'pigs')

        @campaign_button.event("on_click")
        def on_click_campaign_button(event):
            logging.debug(event)
            self.on_campaign()

        @options_button.event("on_click")
        def on_click_options_button(event):
            logging.debug(event)
            # Pass already created view because we are resuming.

            self.window.show_view(
                SettingsMenu(
                    self.window,
                    self.state,
                    previous_view=self,
                    shadertoy=self.shadertoy, time=self.time
                )
            )

        @quit_button.event("on_click")
        def on_click_quit_button(event):
            logging.debug(event)
            self.fade_quit()

        widgets = [
            label,
            campaign_button
        ]

        widgets += [
            options_button,
            quit_button
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=20, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout())
        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

    def on_show_view(self) -> None:
        """ On show view """
        super().on_show_view()
        self.state.settings.unmute()
        self.window.set_mouse_visible(True)
        self.push_controller_handlers()

        music = None

        try:

            music = arcade.load_sound(
                os.path.join(self.state.music_dir, 'menu.ogg'),
                streaming=streaming_enabled()
            )
        except FileNotFoundError as e:
            logging.error(e)

        if not self.player and music:
            self.player = music.play(loop=True,
                                     volume=self.state.settings.music_volume * self.state.settings.master_volume)

        self.manager.enable()

    def on_hide_view(self) -> None:
        """ On hide view """

        super().on_hide_view()
        self.pop_controller_handlers()
        self.manager.disable()

        if self.next_view:
            if self.player:
                self.player.pause()

    def on_campaign(self) -> None:
        """ On click "New Game" show difficulty selection """
        self._fade_in = None

        self.window.show_view(
            CampaignMenu(
                self.window,
                self.state,
                previous_view=self,
                shadertoy=self.shadertoy,
                time=self.time,
                player=self.player
            )
        )

    def on_update(self, delta_time: float) -> None:
        """ on update """

        super().on_update(delta_time=delta_time)

        self.update_mouse()
        self.update_fade(self.next_view)

        # The animation gets distorted after some time
        if self.time >= 480:
            self.time = 0

        volume = self.state.settings.music_volume * self.state.settings.master_volume

        if self.player and self.player.volume != volume:
            self.player.volume = volume

    def on_draw(self) -> None:
        """ on draw """

        self.camera_gui.use()
        self.render_shadertoy()

        self.manager.draw()

        self.draw_fading()
        self.draw_after(draw_version_number=True)
