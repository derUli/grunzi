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
IMAGE_SIZE = (256, 256)

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

        self.maps = SaveGameState.load().get_selectable()

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

        title = arcade.gui.UILabel(
            text=_('Select Map'),
            font_name=FONT_DEFAULT,
            font_size=utils.text.FONT_SIZE_HEADLINE,
            text_color=arcade.csscolor.HOTPINK,
            align='center'
        )

        buttons = arcade.gui.UIBoxLayout(space_between=40, align='center', vertical=False).with_padding(top=40)

        for map in self.maps:
            image = PIL.Image.open(
                os.path.join(self.state.ui_dir, 'map_previews', f"{map}.jpg")
            ).convert('RGBA').crop()

            image.resize(IMAGE_SIZE)

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

            texture_default = arcade.texture.Texture(
                name=f"preview-{map}-default",
                image=image_normal
            )
            texture_hovered = arcade.texture.Texture(
                name=f"preview-{map}-hovered",
                image=image_hovered
            )

            button = arcade.gui.UITextureButton(
                width=image_normal.width,
                height=image_normal.height,
                texture=texture_default,
                texture_hovered=texture_hovered,
                style=utils.gui.get_button_style()
            )

            self.map_buttons[map] = button

            @button.event('on_click')
            def on_select_level(event):
                self.on_select_level(event)

            buttons.add(button)

        widgets = [
            back_button,
            title,
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

        # Clear the screen
        self.clear()
        self.camera_gui.use()
        self.render_shadertoy()
        self.manager.draw()

        self.draw_fading()
        self.draw_after(draw_version_number=True)

    def on_back(self) -> None:
        """ On back """

        from views.mainmenu import MainMenu
        self.fade_to_view(MainMenu(self.window, self.state))

    def on_select_level(self, event):
        for map in self.map_buttons:
            if self.map_buttons[map] != event.source:
                continue

            savegame = SaveGameState.load()
            self.state.map_name = map
            self.state.difficulty = MapConfig(savegame.difficulty, map, self.state.map_dir)

            self.fade_to_view(Game(self.window, self.state))
