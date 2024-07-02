import logging
import time

import arcade

from constants.collisions import COLLISION_BULLET, COLLISION_PLAYER, COLLISION_SLIMER_BULLET
from constants.layers import LAYER_NPC
from sprites.bullet.bullet import Bullet
from sprites.characters.character import Character
from state.argscontainer import ArgsContainer
from utils.physics import on_hit_destroy

MASS = 1

DAMPING = 1
FRICTION = 1
ELASTICITY = 0.1
FORCE_MOVE = 50000

SIGHT_DISTANCE = 1000
DESTROY_TIME = 3
FADE_ALPHA_SPEED = 1

COLOR = (124, 252, 0, 255)


class SlimerBullet(Bullet):

    def __init__(
            self,
            radius=64,
            color=COLOR,
            soft=True,
            force_move=FORCE_MOVE,
            hurt=30
    ):
        super().__init__(radius, color, soft, force_move, hurt)

        self.radius = radius

    def setup(self, source, physics_engine, scene, state, target=None):

        force_x = 0
        force_y = 0

        self.center_x = source.center_x
        self.center_y = source.center_y
        self.alpha = 0

        if target.left > source.right:
            self.left = source.right
            force_x = FORCE_MOVE
        else:
            self.right = source.left
            force_x = FORCE_MOVE * -1

        original_center_x = self.center_x

        self.alpha = 0

        can_hit = False

        for i in range(1, 1000):
            self.center_x += i
            if arcade.check_for_collision(self, target):
                can_hit = True

        self.center_x = original_center_x

        for i in range(1, 1000):
            self.center_x -= i
            if arcade.check_for_collision(self, target):
                can_hit = True

        if not can_hit:
            self.remove_from_sprite_lists()
            return

        self.center_x = original_center_x
        self.alpha = 255

        scene.add_sprite(LAYER_NPC, self)

        # TODO: Other sound effect
        state.play_sound('shot', speed=0.1)
        physics_engine.add_sprite(
            self,
            mass=MASS,
            damping=DAMPING,
            friction=FRICTION,
            collision_type=COLLISION_SLIMER_BULLET,
            elasticity=ELASTICITY
        )

        physics_engine.add_collision_handler(
            COLLISION_SLIMER_BULLET,
            COLLISION_SLIMER_BULLET,
            post_handler=on_hit_destroy
        )

        physics_engine.add_collision_handler(
            COLLISION_SLIMER_BULLET,
            COLLISION_BULLET,
            post_handler=self.on_hit_shrink
        )

        physics_engine.apply_force(self, (force_x, force_y))

        physics_engine.add_collision_handler(
            COLLISION_SLIMER_BULLET,
            COLLISION_PLAYER,
            post_handler=self.on_hit_player
        )

    def on_hit_shrink(self, bullet_sprite, _hit_sprite, _arbiter, _space, _data):
        scale_sub = 0.2 * _hit_sprite.hurt_modifier
        scale = self.scale - scale_sub

        _hit_sprite.remove_from_sprite_lists()

        if scale <= 0:
            self.remove_from_sprite_lists()
            return

        self.scale = scale

    def on_hit_player(self, bullet_sprite, _hit_sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        bullet_sprite.remove_from_sprite_lists()
        if not isinstance(_hit_sprite, Character):
            return

        hurt = self.hurt

        _hit_sprite.hurt(hurt)

    def update(
            self,
            delta_time: float,
            args: ArgsContainer
    ) -> None:
        """
        Update bullet

        @param delta_time: Delta Time
        @param args: arguments container
        """
        new_alpha = self.alpha - FADE_ALPHA_SPEED
        if time.time() >= self.created_at + DESTROY_TIME and self.alpha >= 255:
            logging.debug('Remove slimer bullet from scene')

        if new_alpha > 0:
            self.alpha = new_alpha
        else:
            self.remove_from_sprite_lists()
