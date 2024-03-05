""" Player sprite class """

import arcade
from arcade import FACE_RIGHT

from sprites.characters.enemysprite import EnemySprite
from sprites.characters.spritehealth import HEALTH_FULL, HEALTHBAR_FREN_COLOR

FADE_SPEED = 5
DEFAULT_FACE = FACE_RIGHT
MOVE_DAMPING = 0.01

class Ferret(EnemySprite):
    def __init__(
            self,
            filename: str = None,
            center_x = 0,
            center_y = 0
    ):
        super().__init__(filename, center_x=center_x, center_y=center_y)

        self.textures = arcade.load_texture_pair(filename)

        self.texture = self.textures[0]
        self.health = HEALTH_FULL
        self._died = False

        self.damping = MOVE_DAMPING

    def draw_overlay(self):
        self.draw_healthbar(HEALTHBAR_FREN_COLOR)

    def draw_debug(self):
        pass

    def update(
            self,
            player=None,
            scene=None,
            physics_engine=None,
            state=None,
            delta_time=None,
            map_size=None
    ):
        if self.dead:
            alpha = self.alpha - FADE_SPEED

            if alpha <= 0:
                alpha = 0
                self.remove_from_sprite_lists()

            self.alpha = alpha

            return
