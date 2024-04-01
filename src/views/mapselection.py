import logging
import os

import arcade.gui

import constants.controls.keyboard
import utils.gui
import utils.text
from constants.difficulty import Difficulty
from constants.fonts import FONT_DEFAULT
from state.savegamestate import SaveGameState, new_savegame
from views.fading import Fading
from views.game import Game

BUTTON_WIDTH = 250


class MapSelection(Fading):
    """Main menu view class."""

    def __init__(self, window, state, previous_view):
        super().__init__(window)

        self.window = window
        self.state = state
        self.previous_view = previous_view
        self.manager = arcade.gui.UIManager(window)
        self.shadertoy = self.state.load_shader(window.size, 'pink')
        self.time = 0

        self.difficulty = None
        self.maps = []
        self.select_button = None
        self.selected = 0

    def on_show_view(self):
        """ This is run once when we switch to this view """
        super().on_show_view()

        self.push_controller_handlers()
        self.window.set_mouse_visible(True)

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])

        self.setup()

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.pop_controller_handlers()
        self.manager.disable()

        if self.previous_view.player:
            self.previous_view.player.pause()

    def setup(self):
        self.manager.clear()
        self.manager.disable()
        self.maps = SaveGameState.load().get_selectable()

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        @back_button.event("on_click")
        def on_click_back_button(event):
            # Pass already created view because we are resuming.

            self.on_back()

        title = arcade.gui.UILabel(
            text=_('Select Map'),
            font_name=FONT_DEFAULT,
            font_size=utils.text.HEADLINE_FONT_SIZE,
            text_color=arcade.csscolor.HOTPINK,
            align='center'
        )

        buttons = arcade.gui.UIBoxLayout(space_between=40, align='center', vertical=False)

        button_prev = arcade.gui.UITextureButton(
            texture=arcade.load_texture(
                os.path.join(self.state.image_dir, 'ui', 'arrows', 'left.png')
            )
        )

        button_next = arcade.gui.UITextureButton(
            texture=arcade.load_texture(
                os.path.join(self.state.image_dir, 'ui', 'arrows', 'right.png')
            )
        )

        @button_prev.event('on_click')
        def on_click_button_prev(event):
            if self.selected > 0:
                self.selected -= 1
            else:
                self.selected = len(self.maps) - 1

            self.setup()

        @button_next.event('on_click')
        def on_click_button_next(event):
            if self.selected < len(self.maps) - 1:
                self.selected += 1
            else:
                self.selected = 0

            self.setup()

        select_button = arcade.gui.UIFlatButton(
            text=self.maps[self.selected],
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        @select_button.event('on_click')
        def on_start_map(event):
            map = event.source.text

            savegame = SaveGameState.load()
            self.state.map_name = map
            self.state.difficulty = Difficulty(savegame.difficulty)

            self.next_view = Game(self.window, self.state)
            self.fade_out()
            # self.on_start_map()

        buttons.add(button_prev)
        buttons.add(select_button)
        buttons.add(button_next)

        widgets = [
            title,
            back_button,
            buttons
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=10, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout())
        frame.with_padding(bottom=20)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.manager.enable()

        if self.previous_view.player:
            self.previous_view.player.play()

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

    def on_select_difficulty(self, difficulty, overwrite=False):
        self.difficulty = difficulty

        if SaveGameState.exists() and not overwrite:
            return self.on_confirm_overwrite_savegame()

        logging.info(utils.text.label_value('Difficulty', difficulty))

        if self.previous_view.player:
            self.previous_view.player.pause()

        new_savegame(self.state.map_name_first, difficulty)

        self.state.map_name = self.state.map_name_first
        self.state.difficulty = Difficulty(difficulty)

        from views.game import Game

        self.next_view = Game(self.window, self.state)
        self.fade_out()

    def on_back(self):
        from views.mainmenu import MainMenu
        self.next_view = MainMenu(self.window, self.state)
        self.fade_out()

    def on_confirm_overwrite_savegame(self):
        message_box = arcade.gui.UIMessageBox(
            width=300,
            height=200,
            message_text=_('Overwrite existing savegame?'),
            buttons=[
                _("Yes"),
                _("No")
            ]
        )

        message_box.on_action = self.on_overwrite_savegame

        self.manager.add(message_box)

    def on_overwrite_savegame(self, event):
        action = event.action
        if action == _('Yes'):
            self.on_select_difficulty(self.difficulty, overwrite=True)