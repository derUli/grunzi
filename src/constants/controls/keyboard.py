"""Keyboard controls"""
import arcade

KEY_PAUSE = [arcade.key.ESCAPE]
KEY_DISCARD = [
    arcade.key.ESCAPE,
    arcade.key.ENTER,
    arcade.key.NUM_ENTER,
    arcade.key.SPACE
]
KEY_SPRINT = [arcade.key.LSHIFT, arcade.key.RSHIFT]
KEY_SHOOT = [arcade.key.LCTRL, arcade.key.RCTRL]
KEY_GRUNT = [arcade.key.G]
KEY_USE = [arcade.key.E]
KEY_DROP = [arcade.key.Q]

KEY_MOVE_LEFT = [arcade.key.LEFT, arcade.key.A]
KEY_MOVE_RIGHT = [arcade.key.RIGHT, arcade.key.D]
KEY_MOVE_UP = [arcade.key.UP, arcade.key.W]
KEY_MOVE_DOWN = [arcade.key.DOWN, arcade.key.S]

KEY_SELECT_INVENTORY = [
    arcade.key.KEY_0,
    arcade.key.KEY_1,
    arcade.key.KEY_2,
    arcade.key.KEY_3,
    arcade.key.KEY_4,
    arcade.key.KEY_5
]

KEY_SCREENSHOT = [arcade.key.F12]
KEY_TOGGLE_FPS = [arcade.key.F3]
KEY_TOGGLE_DEBUG = [arcade.key.F4]
