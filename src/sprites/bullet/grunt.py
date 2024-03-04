import arcade
from arcade import FACE_RIGHT, FACE_LEFT

import views.game
from sprites.characters.enemysprite import EnemySprite
from constants.layers import SPRITE_LIST_ENEMIES
MASS = 1
DAMPING = 1
FRICTION = 1
ELASTICITY = 0.1

FORCE_MOVE = 20000


class Grunt(arcade.sprite.SpriteCircle, EnemySprite):
    def __init__(
            self,
            radius,
            color=arcade.csscolor.WHITE,
            soft=False,
            force_move=FORCE_MOVE
    ):
        super().__init__(radius, color=color, soft=soft)

        self.force_move = force_move

        self.sound = None
        self.alpha = 0

    def draw_debug(self):
        pass

    def draw_overlay(self):
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

        if self.sound and not self.sound.playing:
            self.remove_from_sprite_lists()

    def setup(self, source, physics_engine, scene, state, sound=True):

        self.center_y = source.center_y

        if source.face == FACE_RIGHT:
            self.right = source.right + self.width * 2
        elif source.face == FACE_LEFT:
            self.force_move = -self.force_move
            self.left = source.left - self.width

        scene.add_sprite(SPRITE_LIST_ENEMIES, self)

        if sound:
            self.sound = state.grunt()

        physics_engine.add_sprite(
            self,
            mass=MASS,
            damping=DAMPING,
            friction=FRICTION,
            collision_type="grunt",
            elasticity=ELASTICITY
        )

        physics_engine.apply_force(self, (self.force_move, 0))
        physics_engine.add_collision_handler('grunt', 'enemy', post_handler=self.on_hit)

    def on_hit(self, sprite, _hit_sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        self.remove_from_sprite_lists()
