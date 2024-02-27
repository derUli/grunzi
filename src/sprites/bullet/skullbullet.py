import arcade
from arcade import FACE_RIGHT, FACE_LEFT

import views.game
from sprites.bullet.bullet import Bullet
from sprites.characters.enemysprite import EnemySprite
from sprites.characters.playersprite import PlayerSprite

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

        self.center_y = source.center_y

        force_x = 0
        force_y = 0

        if target.left > source.right:
            self.right = source.right + self.width
            force_x = self.force_move
        else:
            self.left = source.left - self.width
            force_x = -self.force_move

        if target.top > source.bottom:
            self.bottom = source.bottom + self.width
            force_y = self.force_move
        else:
            self.top = source.top + self.width
            force_y = -self.force_move

        scene.add_sprite(views.game.SPRITE_LIST_ENEMIES, self)

        state.play_sound('shot')

        physics_engine.add_sprite(
            self,
            mass=MASS,
            damping=DAMPING,
            friction=FRICTION,
            collision_type="bullet",
            elasticity=ELASTICITY
        )

        physics_engine.add_collision_handler('bullet', 'wall', post_handler=self.on_hit)
        physics_engine.add_collision_handler('bullet', 'player', post_handler=self.on_hit)
        physics_engine.apply_force(self, (force_x, force_y))

    def on_hit(self, bullet_sprite, _hit_sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        if isinstance(_hit_sprite, SkullBullet):
            return

        bullet_sprite.remove_from_sprite_lists()

        if isinstance(_hit_sprite, PlayerSprite):
            _hit_sprite.hurt(5)