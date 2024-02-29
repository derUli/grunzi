""" Player sprite class """

import arcade
from arcade import FACE_RIGHT, FACE_LEFT, FACE_DOWN, FACE_UP

import utils.text
from sprites.characters.spritehealth import HEALTH_FULL, SpriteHealth

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
MOVE_FORCE = 1300

MODIFIER_DEFAULT = 1
MODIFIER_SPRINT = 2

MOVE_DAMPING = 0.01

HEALTH_REGENERATION_SPEED = 0.1

FULL_ALPHA = 255
ONE_PERCENT_ALPHA = FULL_ALPHA / 100

PLACE_ITEM_ALPHA = 100

class PlayerSprite(arcade.sprite.Sprite, SpriteHealth):
    def __init__(
            self,
            filename: str = None,
    ):
        super().__init__()

        self.move_force = MOVE_FORCE
        self.modifier = MODIFIER_DEFAULT
        self.damping = MOVE_DAMPING
        self.textures = arcade.load_texture_pair(filename)

        self.health = HEALTH_FULL

        self.face = DEFAULT_FACE
        self.texture = self.textures[self.face - 1]

        self.scale = 0.9
        self.item = None

    def update_texture(self):
        if self.face > len(self.textures):
            return

        self.texture = self.textures[self.face - 1]

    def reset(self):
        self.modifier = MODIFIER_DEFAULT

    def update(self):
        if self.dead():
            return

        if self.health < HEALTH_FULL:
            self.health += HEALTH_REGENERATION_SPEED

        if self.health > HEALTH_FULL:
            self.health = HEALTH_FULL

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.face = FACE_LEFT
            self.update_texture()
        elif self.change_x > 0:
            self.face = FACE_RIGHT
            self.update_texture()
        elif self.change_y > 0:
            self.face = FACE_DOWN
        elif self.change_y < 0:
            self.face = FACE_UP

        if self.item:
            if self.face == FACE_RIGHT:
                self.item.left = self.right
                self.item.center_y = self.center_y
                self.alpha = PLACE_ITEM_ALPHA
            elif self.face == FACE_LEFT:
                self.item.right = self.left
                self.item.center_y = self.center_y
                self.item.alpha = PLACE_ITEM_ALPHA
            elif self.face == FACE_UP:
                self.item.center_x = self.center_x
                self.item.bottom = self.top
            elif self.face == FACE_DOWN:
                self.item.center_x = self.center_x
                self.item.top = self.bottom

            self.item.draw()

    def draw_overlay(self):
        window = arcade.get_window()

        if self.health >= HEALTH_FULL:
            return

        alpha = FULL_ALPHA - self.health * ONE_PERCENT_ALPHA

        arcade.draw_rectangle_filled(window.width / 2, window.height / 2,
                                     window.width, window.height,
                                     (255, 0, 0, alpha))

        if not self.dead():
            return

        # TODO: Implement real game over screen
        utils.text.create_text(
            _("You're bacon!"),
            width=window.width - (utils.text.MARGIN * 2),
            align='left').draw()

    def set_item(self, item):
        if self.item:
            self.item.alpha = 255

        self.item = item
        return item