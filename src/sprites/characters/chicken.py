""" Player sprite class """
import logging
import os
import random

import arcade
from arcade import FACE_RIGHT, PymunkPhysicsEngine, FACE_LEFT

from constants.collisions import COLLISION_CHICKEN
from constants.layers import all_layers, LAYER_ENEMIES, LAYER_FEATHER
from sprites.characters.character import Character
from sprites.characters.spritehealth import HEALTH_FULL, HEALTHBAR_FREN_COLOR
from sprites.items.item import Useable
from sprites.items.redherring import Feather
from utils.positional_sound import PositionalSound
from utils.sprite import random_position

FADE_SPEED = 4
DEFAULT_FACE = FACE_RIGHT
MOVE_DAMPING = 0.01
MOVE_FORCE = 2000


class Chicken(Character, Useable):
    def __init__(
            self,
            filename: str = None,
            center_x=0,
            center_y=0
    ):
        super().__init__(filename, center_x=center_x, center_y=center_y)

        self.textures = arcade.load_texture_pair(filename)
        self.face = DEFAULT_FACE
        self.face_horizontal = DEFAULT_FACE
        self.texture = self.textures[self.face - 1]

        self.force_move = MOVE_FORCE
        self.health = HEALTH_FULL
        self._died = False

        self.damping = MOVE_DAMPING
        self.sound = None

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
            if self.sound:
                self.sound.pause()

            alpha = self.alpha - FADE_SPEED

            if alpha <= 0:
                alpha = 0

                feather = Feather(
                    filename=os.path.join(state.sprite_dir, 'tools', 'feather.png')
                )
                feather.center_x = self.center_x
                feather.center_y = self.center_y

                scene.add_sprite(LAYER_FEATHER, feather)

                self.remove_from_sprite_lists()

            self.alpha = alpha

            return

        move_x = 0
        move_y = 0

        if random.randint(1, 80) == 50:
            move_x = random.choice([-self.force_move, self.force_move])
        if random.randint(1, 80) == 50:
            move_y = random.choice([-self.force_move, self.force_move])

        if move_x > 0:
            self.face = FACE_RIGHT
            self.face_horizontal = FACE_RIGHT
            self.texture = self.textures[self.face_horizontal - 1]
        elif move_x < 0:
            self.face = FACE_LEFT
            self.face_horizontal = FACE_LEFT
            self.texture = self.textures[self.face_horizontal - 1]

        physics_engine.apply_force(self, (move_x, move_y))

        # randomize play sound
        if random.randint(1, 50) == 30:
            self.play_sound(player=player, state=state)

        if self.sound:
            self.sound.update()

    def play_sound(self, player, state):
        if self.sound and self.sound.playing:
            return

        audio = state.play_sound('chicken' + str(random.randint(1, 6)))
        self.sound = PositionalSound(player, self, audio, state)
        self.sound.play()


def spawn_chicken(state, tilemap, scene, physics_engine):
    rand_x, rand_y = random_position(tilemap)

    chicken = Chicken(
        filename=os.path.join(state.sprite_dir, 'char', 'chicken.png'),
        center_x=rand_x,
        center_y=rand_y
    )

    try:
        if arcade.check_for_collision_with_list(chicken, all_layers(scene)):
            return spawn_chicken(state, tilemap, scene, physics_engine)
    except AttributeError as e:
        logging.error(e)
        return

    scene.add_sprite(LAYER_ENEMIES, chicken)
    physics_engine.add_sprite(
        chicken,
        moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
        collision_type=COLLISION_CHICKEN
    )
