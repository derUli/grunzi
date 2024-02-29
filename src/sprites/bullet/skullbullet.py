import arcade

import views.game
from sprites.bullet.bullet import Bullet

HURT = 10

MASS = 0.1
DAMPING = 1
FRICTION = 1
ELASTICITY = 0.1
FORCE_MOVE = 2000


class SkullBullet(Bullet):

    def __init__(
            self,
            radius,
            color=arcade.csscolor.BLACK,
            soft=False,
            force_move=FORCE_MOVE,
            hurt=HURT
    ):
        super().__init__(radius, color, soft, force_move, hurt)

        self.target = None

    def setup(self, source, physics_engine, scene, state, target=None):

        force_x = 0
        force_y = 0

        if target.left > source.right:
            self.right = source.right
            force_x = self.force_move
        elif target.left < source.right:
            self.left = source.left
            force_x = -self.force_move

        if target.top > source.bottom:
            self.top = source.top
            force_y = self.force_move
        elif target.top < source.bottom:
            self.bottom = source.bottom
            force_y = -self.force_move

        scene.add_sprite(views.game.SPRITE_LIST_ENEMIES, self)

        state.play_sound('shot')

        physics_engine.add_sprite(
            self,
            mass=MASS,
            damping=DAMPING,
            friction=FRICTION,
            collision_type="skull_bullet",
            elasticity=ELASTICITY
        )

        physics_engine.add_collision_handler('skull_bullet', 'wall', post_handler=self.on_hit_destroy)
        physics_engine.add_collision_handler('skull_bullet', 'player', post_handler=self.on_hit_player)  #
        physics_engine.apply_force(self, (force_x, force_y))

    def on_hit_destroy(self, bullet_sprite, _hit_sprite, _arbiter, _space, _data):
        bullet_sprite.remove_from_sprite_lists()

    def on_hit_player(self, bullet_sprite, _hit_sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        bullet_sprite.remove_from_sprite_lists()

        _hit_sprite.hurt(10)
