import arcade
from arcade import SpriteSolidColor

from constants.collisions import COLLISION_BULLET, COLLISION_WALL, COLLISION_SKULL_BULLET, COLLISION_PLAYER, \
    COLLISION_CHICKEN
from constants.layers import LAYER_ENEMIES
from sprites.bullet.bullet import Bullet
from sprites.characters.character import Character
from sprites.characters.chicken import Chicken
from utils.physics import on_hit_destroy

MASS = 0.1
DAMPING = 1
FRICTION = 1
ELASTICITY = 0.1
FORCE_MOVE = 4000

SIGHT_DISTANCE = 10000

HURT_CHICKEN = 35

class SkullBullet(Bullet):

    def __init__(
            self,
            radius,
            color=arcade.csscolor.BLACK,
            soft=False,
            force_move=FORCE_MOVE,
            hurt=10
    ):
        super().__init__(radius, color, soft, force_move, hurt)

        self.target = None

    def setup(self, source, physics_engine, scene, state, target=None):

        force_x = 0
        force_y = 0

        self.center_x = source.center_x
        self.top = source.center_y

        # Check if should shoot up
        collision_sprite_up = SpriteSolidColor(
            width=int(source.width),
            height=SIGHT_DISTANCE,
            color=arcade.csscolor.YELLOW
        )
        collision_sprite_up.bottom = source.top
        collision_sprite_up.left = source.left

        # Check if should shoot down
        collision_sprite_down = SpriteSolidColor(
            width=int(source.width),
            height=SIGHT_DISTANCE,
            color=arcade.csscolor.YELLOW
        )
        collision_sprite_down.top = source.bottom
        collision_sprite_down.left = source.left

        # Check if should shoot down
        collision_sprite_left = SpriteSolidColor(
            width=SIGHT_DISTANCE,
            height=int(source.height),
            color=arcade.csscolor.YELLOW
        )
        collision_sprite_left.top = source.top
        collision_sprite_left.right = source.left

        # Check if should shoot right
        collision_sprite_right = SpriteSolidColor(
            width=SIGHT_DISTANCE,
            height=int(source.height),
            color=arcade.csscolor.YELLOW
        )
        collision_sprite_right.top = source.top
        collision_sprite_right.left = source.right

        # Check if should shoot top right
        collision_sprite_topright = SpriteSolidColor(
            width=SIGHT_DISTANCE,
            height=SIGHT_DISTANCE,
            color=arcade.csscolor.YELLOW
        )
        collision_sprite_topright.bottom = source.top
        collision_sprite_topright.left = source.right

        # Check if should shoot bottom right
        collision_sprite_bottomright = SpriteSolidColor(
            width=SIGHT_DISTANCE,
            height=SIGHT_DISTANCE,
            color=arcade.csscolor.YELLOW
        )
        collision_sprite_bottomright.top = source.bottom
        collision_sprite_bottomright.left = source.right

        # Check if should shoot top right
        collision_sprite_topleft = SpriteSolidColor(
            width=SIGHT_DISTANCE,
            height=SIGHT_DISTANCE,
            color=arcade.csscolor.YELLOW
        )
        collision_sprite_topleft.bottom = source.top
        collision_sprite_topleft.right = source.left

        # Check if should shoot top right
        collision_sprite_bottomleft = SpriteSolidColor(
            width=SIGHT_DISTANCE,
            height=SIGHT_DISTANCE,
            color=arcade.csscolor.YELLOW
        )
        collision_sprite_bottomleft.top = source.bottom
        collision_sprite_bottomleft.right = source.left

        if arcade.check_for_collision(collision_sprite_up, target):
            self.bottom = source.top
            force_y = self.force_move
        elif arcade.check_for_collision(collision_sprite_down, target):
            self.top = source.bottom
            force_y = -self.force_move
        elif arcade.check_for_collision(collision_sprite_left, target):
            self.right = source.left
            force_x = -self.force_move
        elif arcade.check_for_collision(collision_sprite_right, target):
            self.left = source.right
            force_x = self.force_move
        elif arcade.check_for_collision(collision_sprite_topright, target):
            self.bottom = source.top
            force_x = self.force_move
            force_y = self.force_move
        elif arcade.check_for_collision(collision_sprite_bottomright, target):
            self.top = source.bottom
            force_x = self.force_move
            force_y = -self.force_move
        elif arcade.check_for_collision(collision_sprite_topleft, target):
            self.bottom = source.top
            force_x = -self.force_move
            force_y = self.force_move
        elif arcade.check_for_collision(collision_sprite_bottomleft, target):
            self.top = source.bottom
            force_x = -self.force_move
            force_y = -self.force_move
        else:
            self.remove_from_sprite_lists()
            return

        scene.add_sprite(LAYER_ENEMIES, self)

        state.play_sound('shot')

        physics_engine.add_sprite(
            self,
            mass=MASS,
            damping=DAMPING,
            friction=FRICTION,
            collision_type=COLLISION_SKULL_BULLET,
            elasticity=ELASTICITY
        )

        physics_engine.add_collision_handler(
            COLLISION_SKULL_BULLET,
            COLLISION_WALL,
            post_handler=on_hit_destroy
        )

        physics_engine.add_collision_handler(
            COLLISION_SKULL_BULLET,
            COLLISION_SKULL_BULLET,
            post_handler=on_hit_destroy
        )

        physics_engine.add_collision_handler(
            COLLISION_SKULL_BULLET,
            COLLISION_BULLET,
            post_handler=on_hit_destroy
        )

        physics_engine.apply_force(self, (force_x, force_y))

        physics_engine.add_collision_handler(
            COLLISION_SKULL_BULLET,
            COLLISION_PLAYER,
            post_handler=self.on_hit_player
        )

        physics_engine.add_collision_handler(
            COLLISION_SKULL_BULLET,
            COLLISION_CHICKEN,
            post_handler=self.on_hit_player
        )

    def on_hit_player(self, bullet_sprite, _hit_sprite, _arbiter, _space, _data):
        """ Called for bullet/wall collision """
        bullet_sprite.remove_from_sprite_lists()
        if not isinstance(_hit_sprite, Character):
            return

        hurt = self.hurt

        if isinstance(_hit_sprite, Chicken):
            hurt = HURT_CHICKEN

        _hit_sprite.hurt(hurt)
