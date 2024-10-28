""" Player sprite class """
import logging
import os
import random

import arcade
from arcade import FACE_RIGHT, PymunkPhysicsEngine, FACE_LEFT

from constants.collisions import COLLISION_CHICKEN
from constants.layers import LAYER_NPC, LAYER_FEATHER, check_collision_with_layers
from sprites.characters.character import Character
from sprites.characters.spritehealth import HEALTH_FULL, HEALTHBAR_FREN_COLOR
from sprites.items.item import Useable
from sprites.items.redherring import Feather
from state.argscontainer import ArgsContainer
from utils.animationconfig import AnimationConfig
from utils.characteranimation import CharacterAnimation
from utils.positionalsound import PositionalSound
from utils.sprite import random_position

FADE_SPEED = 4
DEFAULT_FACE = FACE_RIGHT
MOVE_DAMPING = 0.01
MOVE_FORCE = 2000
HEALTH_EMPTY = 0

ANIMATION_IDLE = 'idle.png'


ANIMATIONS_ALL = {
    ANIMATION_IDLE: AnimationConfig(size=(375, 591), loop=True, frame_length=0.2, apply_modifier=False)
}


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
        self.initialized = False
        self.force_move = MOVE_FORCE
        self.health = HEALTH_FULL
        self._died = False
        self.animations = {}
        self.damping = MOVE_DAMPING
        self.sound = None
        self._current_animation = ANIMATION_IDLE

    def draw_overlay(self, args: ArgsContainer):
        self.draw_healthbar(HEALTHBAR_FREN_COLOR)


    def setup(self, args):
        self.initialized = True

        for anim in ANIMATIONS_ALL:
            animation = CharacterAnimation()
            config = ANIMATIONS_ALL[anim]
            animation.load(
                state=args.state,
                filename=anim,
                size=config.size,
                loop=config.loop,
                frame_length=config.frame_length,
                apply_modifier=config.apply_modifier,
                character='chicken',
                resize=(32, 50)
            )
            self.animations[anim] = animation


    def update(
            self,
            delta_time: float,
            args: ArgsContainer
    ) -> None:
        if not self.initialized:
            self.setup(args)

        if self.current_animation and self.current_animation.update():
            self.textures = self.current_animation.current_frame
            self.texture = self.textures[self.face - 1]

        if self.dead:
            if self.sound:
                self.sound.pause()

            alpha = self.alpha - FADE_SPEED

            if alpha <= 0:
                alpha = 0

                feather = Feather(
                    filename=os.path.join(args.state.sprite_dir, 'tools', 'feather.png')
                )
                feather.center_x = self.center_x
                feather.center_y = self.center_y

                args.scene.add_sprite(LAYER_FEATHER, feather)

                self.remove_from_sprite_lists()

            self.alpha = alpha

            return

        if self.sound and self.sound.playing:
            self.sound.update()
            return

        # randomize play sound
        if random.randint(1, 50) == 30:
            self.play_sound(player=args.player, state=args.state)

    def play_sound(self, player, state) -> None:
        if self.sound and self.sound.playing:
            return

        audio = state.play_sound('chicken' + str(random.randint(1, 6)))
        self.sound = PositionalSound(player, self, audio, state)
        self.sound.play()

    @property
    def current_animation(self):
        return self.animations[self._current_animation]

    @current_animation.setter
    def current_animation(self, value):
        if self._current_animation != value:

            if self.current_animation and not self.current_animation.loop and not self.current_animation.completed:
                return

            self._current_animation = value
            self.animations[value].reset()

def spawn_chicken(state, tilemap, scene, physics_engine):
    rand_x, rand_y = random_position(tilemap)

    chicken = Chicken(
        filename=os.path.join(state.sprite_dir, 'char', 'chicken', 'default.png'),
        center_x=rand_x,
        center_y=rand_y
    )

    try:
        if check_collision_with_layers(scene, chicken):
            return spawn_chicken(state, tilemap, scene, physics_engine)
    except AttributeError as e:
        logging.error(e)
        return

    scene.add_sprite(LAYER_NPC, chicken)
    physics_engine.add_sprite(
        chicken,
        moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
        collision_type=COLLISION_CHICKEN
    )

