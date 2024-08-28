""" Pig bullet """
import logging
import math
import time

import arcade
import pymunk
from arcade import FACE_RIGHT, FACE_LEFT, Color

from constants.collisions import COLLISION_ENEMY, COLLISION_BULLET, COLLISION_WALL, COLLISION_CHICKEN, \
    COLLISION_MOVEABLE
from constants.layers import LAYER_NPC
from sprites.characters.barrel import Barrel
from sprites.characters.boss import Boss
from sprites.characters.character import Character
from sprites.characters.chicken import Chicken
from sprites.characters.slimer import Slimer
from sprites.sprite import AbstractSprite
from state.argscontainer import ArgsContainer
from utils.physics import on_hit_destroy

HURT_DEFAULT = 20
HURT_CHICKEN = 35
HURT_SLIMER = 10
HURT_BARREL = 5
HURT_BOSS = 2

SCORE_HURT_CHICKEN = 25
SCORE_HURT_SKULL = 50
SCORE_HURT_SLIMER = 100
SCORE_HURT_BARREL = 200
SCORE_HURT_BOSS = 300

MASS = 0.05
DAMPING = 1
FRICTION = 1
ELASTICITY = 0.1
FORCE_MOVE = 3800

# Destroy after X seconds
DESTROY_TIME = 3


class Bullet(AbstractSprite, arcade.sprite.SpriteCircle):
    def __init__(
            self,
            radius: int,
            color: Color = arcade.csscolor.BLACK,
            soft: bool = False,
            force_move: int = FORCE_MOVE,
            hurt: int = HURT_DEFAULT,
            hurt_modifier: float = 1.0
    ):
        super().__init__(radius, color=color, soft=soft)

        self.force_move = force_move
        self.hurt = hurt
        self.hurt_modifier = hurt_modifier
        self.created_at = time.time()
        self.state = None

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
        if time.time() >= self.created_at + DESTROY_TIME:
            logging.debug('Remove bullet from scene')
            self.remove_from_sprite_lists()

    def setup(self, source, physics_engine, scene, state):

        self.state = state
        self.center_y = source.center_y

        if source.face_horizontal == FACE_RIGHT:
            self.right = source.right + self.width
        elif source.face_horizontal == FACE_LEFT:
            self.force_move = -self.force_move
            self.left = source.left - self.width

        state.play_sound('shot')

        scene.add_sprite(LAYER_NPC, self)
        physics_engine.add_sprite(
            self,
            mass=MASS,
            damping=DAMPING,
            friction=FRICTION,
            collision_type="bullet",
            elasticity=ELASTICITY
        )

        physics_engine.add_collision_handler(COLLISION_BULLET, COLLISION_WALL, post_handler=on_hit_destroy)
        physics_engine.add_collision_handler(COLLISION_BULLET, COLLISION_BULLET, post_handler=on_hit_destroy)
        physics_engine.add_collision_handler(COLLISION_BULLET, COLLISION_ENEMY, post_handler=self.on_hit)
        physics_engine.add_collision_handler(COLLISION_BULLET, COLLISION_CHICKEN, post_handler=self.on_hit)
        physics_engine.add_collision_handler(COLLISION_BULLET, COLLISION_MOVEABLE, post_handler=self.on_hit)

        physics_engine.apply_force(self, (self.force_move, 0))

        return self

    def on_hit(
            self,
            bullet_sprite: arcade.sprite.Sprite,
            _hit_sprite: arcade.sprite.Sprite,
            _arbiter: pymunk.arbiter.Arbiter,
            _space: pymunk.space.Space,
            _data: dict
    ) -> None:
        """ Called for bullet/wall collision """

        bullet_sprite.remove_from_sprite_lists()

        if not isinstance(_hit_sprite, Character):
            return

        hurt = self.hurt

        score = SCORE_HURT_SKULL

        if isinstance(_hit_sprite, Chicken):
            hurt = HURT_CHICKEN
            score = SCORE_HURT_CHICKEN

        if isinstance(_hit_sprite, Slimer):
            hurt = HURT_SLIMER
            score = SCORE_HURT_SLIMER

        if isinstance(_hit_sprite, Barrel):
            hurt = HURT_BARREL
            score = SCORE_HURT_BARREL

        if isinstance(_hit_sprite, Boss):
            hurt = HURT_BOSS
            score = SCORE_HURT_BOSS

        hurt = hurt * self.hurt_modifier

        self.state.score += math.floor(self.hurt_modifier * score)

        _hit_sprite.hurt(hurt)
