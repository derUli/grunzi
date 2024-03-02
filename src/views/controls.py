import os

import arcade.gui

import constants.controls.keyboard
import utils.text
from views.fading import Fading

BUTTON_WIDTH = 250

URL_GRUNZBABE_AT_X = "https://x.com/GrunzBabe"

MARGIN = 60


class Controls(Fading):
    """Main menu view class."""

    def __init__(self, window, state, previous_view):
        super().__init__(window)

        self.time = 0
        self.window = window
        self.state = state
        self.manager = arcade.gui.UIManager(window)

        size = window.width, window.height
        self.shadertoy = self.state.load_shader(size, 'grass')

        self.previous_view = previous_view

    def on_hide_view(self):
        # Disable the UIManager when the view is hidden.
        self.manager.disable()

    def on_back(self):
        self.next_view = self.previous_view
        self.fade_out()

    def on_show_view(self):
        super().on_show_view()
        """ This is run once when we switch to this view """

        controls = [
            _('Scroll with mousewheel'),
            os.linesep * 3
        ]

        if self.window.controller:
            controls += [_('Keyboard:'), os.linesep * 2]

        controls += [
            (_("WASD, Arrow keys"), _('Walk')),
            (_("Shift"), _('Sprint')),
            (_("Ctrl"), _("Shoot")),
            (_("E"), _("Use")),
            (_("Q"), _("Drop item")),
            (_("G"), _("Grunt")),
            (_("0 - 5"), _("Select item")),
            (_("ESC"), _("Open the pause menu")),
            (_('F3'), _('Show FPS')),
            (_("F12"), _("Make screenshot")),
            (_("Alt + Enter"), _("Toggle fullscreen"))
        ]

        if self.window.controller:
            controls += ['XBOX 360 Controller:', os.linesep * 2]
            controls += [
                (_("Left stick"), _('Walk')),
                (_("Right stick"), _('Look')),
                (_("Left trigger"), _('Sprint')),
                (_("X"), _("Shoot")),
                (_("A"), _("Use")),
                (_("Y"), _("Drop item")),
                (_("B"), _("Grunt")),
                (_("Left Button, Right Button"), _("Select item")),
                (_("Start"), _("Open the pause menu"))
            ]

        text = ''

        for line in controls:
            if isinstance(line, tuple):
                label, value = line
                text = text + utils.text.label_value(label, value) + (os.linesep * 2)
            else:
                text = text + str(line)

        text = text.strip()

        # Makes the background darker
        arcade.set_background_color([rgb - 50 for rgb in arcade.color.DARK_BLUE_GRAY])

        v_box = arcade.gui.UIBoxLayout()

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            stye=utils.text.get_style()
        )

        width = int(BUTTON_WIDTH * 2)
        height = self.window.height - (MARGIN * 3)

        textarea = arcade.gui.UITextArea(
            width=width,
            height=height,
            text=text,
            font_size=18,
            text_color=(255, 255, 255),
            multiline=True,
        )

        @back_button.event("on_click")
        def on_click_back_button(event):
            # Pass already created view because we are resuming.

            self.on_back()

        v_box.add(
            textarea.with_space_around(
                top=MARGIN,
                bottom=MARGIN
            )
        )
        v_box.add(back_button.with_space_around(bottom=MARGIN))

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=v_box
            )
        )
        self.manager.enable()

    def on_key_press(self, key, modifiers):
        super().on_key_press(key, modifiers)

        """Called whenever a key is pressed."""
        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_back()

    def on_update(self, dt):
        self.scene.update()
        self.time += dt

        self.update_fade(self.next_view)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()
        self.camera_gui.use()
        self.shadertoy.render(time=self.time)

        self.manager.draw()
        self.draw_fading()
        self.draw_debug()
