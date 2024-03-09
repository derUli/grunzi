""" Controls views """

import os

import arcade.gui

import constants.controls.keyboard
import utils.text
from views.fading import Fading

BUTTON_WIDTH = 250
MARGIN = 40
FONT_SIZE = 18
TEXT_COLOR = (255, 255, 255)

CONTROLS_KEYBOARD = 'keyboard'
CONTROLS_CONTROLLER = 'controller'

LOWEST_FITTING_RESOLUTION = (1440, 900)


class SettingsControls(Fading):
    """Main menu view class."""

    def __init__(self, window, state, previous_view):
        super().__init__(window)

        self.window = window
        self.state = state
        self.manager = arcade.gui.UIManager(window)
        self.next_view = None

        size = window.width, window.height
        self.shadertoy = self.state.load_shader(size, 'grass')

        self.previous_view = previous_view

        self.show_controls = CONTROLS_KEYBOARD

    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.show_scene()

    def show_scene(self):
        super().on_show_view()
        self.scene = arcade.Scene()
        self.manager.clear()

        controls = []

        if self.window.size < LOWEST_FITTING_RESOLUTION:
            controls += [
                _('Scroll with mousewheel'),
                os.linesep * 3
            ]

        if self.show_controls == CONTROLS_KEYBOARD:
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
                (_("Alt + Enter"), _("Toggle fullscreen")),
                (_('F'), _('Ferret'))
            ]

        if self.show_controls == CONTROLS_CONTROLLER:
            controls += [
                'XBox 360 Controller:',
                os.linesep * 2
            ]
            controls += [
                (_("Left stick"), _('Walk')),
                (_("Right stick"), _('Look')),
                (_("Left trigger"), _('Sprint')),
                (_("X"), _("Shoot")),
                (_("A"), _("Use")),
                (_("Y"), _("Drop item")),
                (_("B"), _("Grunt")),
                (_("Left Bumper, Right Bumper"), _("Select item")),
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

        back_button = arcade.gui.UIFlatButton(
            text=_("Back"),
            width=BUTTON_WIDTH,
            style=utils.text.get_style(),
        )

        if self.show_controls == CONTROLS_KEYBOARD:
            toggle_text = _('Controller')
        else:
            toggle_text = _('Keyboard')

        toggle_button = arcade.gui.UIFlatButton(
            text=_(toggle_text),
            width=BUTTON_WIDTH,
            style=utils.text.get_style(),
        )

        @toggle_button.event('on_click')
        def on_toggle(event):
            if self.show_controls == CONTROLS_KEYBOARD:
                self.show_controls = CONTROLS_CONTROLLER
            else:
                self.show_controls = CONTROLS_KEYBOARD

            self.show_scene()

        width = int(BUTTON_WIDTH * 3)
        height = self.window.height - back_button.height - (MARGIN * 2)

        textarea = arcade.gui.UITextArea(
            width=width,
            height=height,
            text=text,
            font_size=FONT_SIZE,
            text_color=TEXT_COLOR,
            multiline=True,
        )

        @back_button.event("on_click")
        def on_back(event):
            self.on_back()

        # Initialise a BoxLayout in which widgets can be arranged.
        widget_layout = arcade.gui.UIBoxLayout(space_between=MARGIN, align='center')

        buttons = arcade.gui.UIBoxLayout(space_between=MARGIN, align='center', vertical=False)
        buttons.add(back_button)

        if any(self.window.controllers):
            buttons.add(toggle_button)

        widgets = [
            textarea,
            buttons
        ]

        for widget in widgets:
            widget_layout.add(widget)

        frame = self.manager.add(arcade.gui.UIAnchorLayout().with_padding())
        frame.add(child=widget_layout, anchor_x="center_x", anchor_y="center_y")

        self.push_controller_handlers()
        self.manager.enable()

    def on_hide_view(self) -> None:
        """ Disable the UIManager when the view is hidden. """

        self.pop_controller_handlers()
        self.manager.disable()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        super().on_key_press(key, modifiers)

        if key in constants.controls.keyboard.KEY_PAUSE:
            self.on_back()

    def on_update(self, delta_time: float = 0) -> None:
        """ On update
        @param dt: Delta Time
        """

        super().on_update(delta_time=delta_time)

        self.time += delta_time

        self.update_mouse()
        self.update_fade(self.next_view)
        self.scene.update()

    def on_draw(self) -> None:
        """ Render the screen. """
        self.clear()
        self.camera_gui.use()
        self.render_shadertoy()

        self.manager.draw()
        self.draw_fading()
        self.draw_debug()

    def on_back(self) -> None:
        """ Go back to main menu """
        self.next_view = self.previous_view
        self.fade_out()
