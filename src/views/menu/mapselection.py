import logging
import os

import PIL
import arcade.gui
from PIL import ImageOps

import constants.controls.keyboard
import utils.gui
import utils.text
from constants.fonts import FONT_DEFAULT
from constants.mapconfig import MapConfig
from state.savegamestate import SaveGameState
from views.fading import Fading
from views.game import Game

BUTTON_WIDTH = 250

COLOR_BACKGROUND = (217, 102, 157)


class MapSelection(Fading):
    """Main menu view class."""

    def __init__(self, window, state, previous_view):
        super().__init__(window)

        self.window = window
        self.state = state
        self.previous_view = previous_view
        self.manager = arcade.gui.UIManager(window)
        self.shadertoy = self.state.load_shader(window.size, 'pink')

        self.maps = []
        self.map_buttons = {}
        self.background = COLOR_BACKGROUND
        self.selected = None

    def on_show_view(self) -> None:
        """ On show view """
        super().on_show_view()

        self.push_controller_handlers()
        self.window.set_mouse_visible(True)

        self.setup()

    def on_hide_view(self) -> None:
        """ On hide view """

        super().on_hide_view()

        self.pop_controller_handlers()
        self.manager.disable()

        if self.previous_view.player:
            self.previous_view.player.pause()

    def setup(self) -> None:
        """ Setup UI """

        self.manager.clear()
        self.manager.disable()

        savegame = SaveGameState.load()
        self.maps = savegame.get_selectable()

        if not self.selected:
            self.selected = savegame.current

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        @back_button.event("on_click")
        def on_click_back_button(event) -> None:
            logging.debug(event)
            # Pass already created view because we are resuming.

            self.on_back()

        next_button = arcade.gui.UIFlatButton(
            text=_("Continue"),
            width=BUTTON_WIDTH,
            style=utils.gui.get_button_style()
        )

        @next_button.event("on_click")
        def on_click_continue(event) -> None:
            logging.debug(event)
            # Pass already created view because we are resuming.
            self.on_start_level()

        title = arcade.gui.UILabel(
            text=_('Select Map'),
            font_name=FONT_DEFAULT,
            font_size=utils.text.FONT_SIZE_HEADLINE,
            text_color=arcade.csscolor.BLACK,
            bold=True,
            align='center'
        )

        selected_map = arcade.gui.UILabel(
            text=_('Selected:') + ' ' + self.selected_label,
            font_name=FONT_DEFAULT,
            font_size=utils.text.FONT_SIZE_LARGE,
            text_color=arcade.csscolor.BLACK,
            bold=True,
            align='center'
        )

        buttons = arcade.gui.UIBoxLayout(space_between=20, align='center', vertical=False).with_padding(top=40)

        for map in self.maps:
            preview_file = os.path.join(self.state.ui_dir, 'map_previews', f"{map}.jpg")

            if not os.path.exists(preview_file):
                continue

            image = PIL.Image.open(preview_file).convert('RGBA').crop()

            image_size = (224, 224)

            if self.window.width >= 1600:
                image_size = (320, 320)

            image = image.resize(image_size)

            image_normal = ImageOps.expand(
                image,
                border=back_button.style['normal'].border_width,
                fill=back_button.style['normal'].border
            )
            image_hovered = ImageOps.expand(
                image,
                border=back_button.style['hover'].border_width,
                fill=back_button.style['hover'].border
            )
            image_selected = ImageOps.expand(
                image,
                border=back_button.style['hover'].border_width,
                fill=arcade.color.RED
            )

            texture_default = arcade.texture.Texture(
                name=f"preview-{map}-default",
                image=image_normal
            )
            texture_selected = arcade.texture.Texture(
                name=f"preview-{map}-selected",
                image=image_selected
            )
            texture_hovered = arcade.texture.Texture(
                name=f"preview-{map}-hovered",
                image=image_hovered
            )

            if map == self.selected:
                texture_default = texture_selected
                texture_hovered = texture_selected

            button = arcade.gui.UITextureButton(
                width=image_normal.width,
                height=image_normal.height,
                texture=texture_default,
                texture_hovered=texture_hovered,
                texture_pressed=texture_selected,
                style=utils.gui.get_button_style()
            )

            self.map_buttons[map] = button

            @button.event('on_click')
            def on_select_level(event):
                self.on_select_level(event)

            buttons.add(button)

        back_next_buttons = arcade.gui.UIBoxLayout(space_between=40, align='center', vertical=False).with_padding(
            top=40)
        back_next_buttons.add(back_button)
        back_next_buttons.add(next_button)

        widgets = [
            title,
            buttons,
            selected_map,
            back_next_buttons
        ]

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=20, align='center')

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout())
        frame.with_padding(bottom=20)

        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.manager.enable()

        if self.previous_view.player:
            self.previous_view.player.play()

    def on_key_press(self, key, modifiers) -> None:
        """ Called whenever a key is pressed. """

        super().on_key_press(key, modifiers)

        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_back()

    def on_update(self, delta_time: float) -> None:
        """ On update """

        super().on_update(delta_time)

        self.update_mouse()
        self.update_fade(self.next_view)
        self.scene.update()

    def on_draw(self) -> None:
        """ Render the screen. """

        self.camera_gui.use()
        self.render_shadertoy()
        self.manager.draw()

        self.draw_fading()
        self.draw_after(draw_version_number=True)

    def on_back(self) -> None:
        """ On back """

        from views.menu.mainmenu import MainMenu
        self.fade_to_view(MainMenu(self.window, self.state))

    def on_select_level(self, event):
        for map in self.map_buttons:
            if self.map_buttons[map] == event.source:
                self.selected = map
                self.setup()

                return

    def on_start_level(self):
        savegame = SaveGameState.load()
        self.state.map_name = self.selected
        self.state.difficulty = MapConfig(savegame.difficulty, self.selected, self.state.map_dir)

        self.fade_to_view(Game(self.window, self.state))

    @property
    def selected_label(self):
        labels = {
            'map01': _('Having A Pig'),
            'map02': _('Big Major Cay'),
            'map03': _('Teufelsmoor'),
            'map04': _('South Pole'),
            'map05': _('Hell')
        }

        if self.selected in labels:
            return labels[self.selected]

        return self.selected
