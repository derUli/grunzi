""" Slimer sprite class """
import os

import arcade
from arcade import FACE_RIGHT, FACE_LEFT, PymunkPhysicsEngine, SpriteList

from constants.collisions import COLLISION_ENEMY
from constants.layers import LAYER_NPC, check_collision_with_layers
from sprites.characters.character import Character
from sprites.characters.spritehealth import HEALTH_FULL
from sprites.items.item import Useable
from utils.physics import DEFAULT_FRICTION
from utils.sprite import random_position

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
MOVE_FORCE = 300
MOVE_DAMPING = 0.01

SIGHT_DISTANCE = 1400
GRID_SIZE = 128

FADE_IN_MAX = 255
FADE_SPEED = 4

SHOOT_DELTA = 1

PATH_FINDING_INTERVAL = 1


class Slimer(Character, Useable):
    def __init__(
            self,
            filename: str = None,
            center_x=0,
            center_y=0,
    ):
        super().__init__(center_x=center_x, center_y=center_y)

        self.move_force = MOVE_FORCE
        self.damping = MOVE_DAMPING

        self.health = HEALTH_FULL
        self._died = False

        dirname = os.path.join(os.path.dirname(filename))

        self.chasing = None
        self.friction = DEFAULT_FRICTION
        self.face = DEFAULT_FACE
        self.textures = arcade.load_texture_pair(os.path.join(dirname, 'slimer.png'))

        self.fade_in = True
        self.alpha = 0
        self.update_texture()
        self.last_shot = 0
        self.sound = None
        self.bullets = SpriteList(lazy=True, use_spatial_hash=True, visible=False)

    def update_texture(self):
        self.texture = self.textures[self.face - 1]

    def draw_overlay(self, args):
        self.draw_healthbar()

    def update(
            self,
            delta_time,
            args
    ):

        self.last_shot += delta_time

        if self.dead:
            alpha = self.alpha - FADE_SPEED

            if alpha <= 0:
                alpha = 0
                self.remove_from_sprite_lists()

            self.alpha = alpha

            return

        if self.fade_in and self.alpha < FADE_IN_MAX:
            new_alpha = self.alpha + FADE_SPEED

            if new_alpha >= FADE_IN_MAX:
                new_alpha = FADE_IN_MAX
                self.fade_in = False

            self.alpha = new_alpha

            return

        if not self.chasing and arcade.has_line_of_sight(
                self.position,
                args.player.position,
                args.wall_spritelist,
                SIGHT_DISTANCE,
                GRID_SIZE
        ):
            self.chasing = True

            if not self.sound:
                self.sound = args.state.play_sound('slimer')

            if self.sound and not self.sound.playing:
                self.sound = None

        if not self.chasing:
            return

        if arcade.get_distance_between_sprites(self, args.player) > SIGHT_DISTANCE:
            self.chasing = False
            return

        # Figure out if we should face left or right
        if args.player.right < self.left:
            self.face = FACE_LEFT
            self.update_texture()
        elif args.player.left > self.right:
            self.face = FACE_RIGHT
            self.update_texture()

        if self.last_shot < SHOOT_DELTA:
            self.movement(args.player, args.physics_engine)
            return

        self.last_shot = 0

        from sprites.bullet.slimerbullet import SlimerBullet

        bullet = SlimerBullet(hurt=args.state.difficulty.slimer_hurt)

        if bullet.setup(self, args.physics_engine, args.scene, args.state, target=args.player):
            self.bullets.append(bullet)

    def movement(self, target, physics_engine):
        if not self.chasing:
            return

        x1, y1 = self.position
        x2, y2 = target.position

        move_x, move_y = 0, 0
        if x2 > x1:
            move_x = MOVE_FORCE
        else:
            move_x = MOVE_FORCE * -1

        if y2 > y1:
            move_y = MOVE_FORCE
        else:
            move_y = MOVE_FORCE * -1

        if arcade.get_distance_between_sprites(self, target) < self.height:
            move_x *= -1
            move_y *= -1

        if move_x > 0 or move_y > 0:
            physics_engine.apply_force(self, (move_x, move_y))


def spawn_slimer(state, tilemap, scene, physics_engine):
    rand_x, rand_y = random_position(tilemap)

    slimer = Slimer(
        filename=os.path.join(
            state.sprite_dir,
            'monster',
            'slimer',
            'slimer.png'
        ),
        center_x=rand_x,
        center_y=rand_y
    )

    if check_collision_with_layers(scene, slimer):
        return spawn_slimer(state, tilemap, scene, physics_engine)

    scene.add_sprite(LAYER_NPC, slimer)
    physics_engine.add_sprite(
        slimer,
        friction=slimer.friction,
        moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
        collision_type=COLLISION_ENEMY,
        max_velocity=200,
        damping=slimer.damping
    )
