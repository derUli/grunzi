""" Player sprite class """
import logging
import os
import random

import arcade
import pyglet
from arcade import FACE_RIGHT, PymunkPhysicsEngine, FACE_LEFT

from constants.collisions import COLLISION_CHICKEN
from constants.layers import LAYER_NPC, check_collision_with_layers
from sprites.characters.character import Character
from sprites.characters.spritehealth import HEALTH_FULL, HEALTHBAR_FREN_COLOR
from sprites.items.item import Useable
from state.argscontainer import ArgsContainer
from utils.animationconfig import AnimationConfig
from utils.characteranimation import CharacterAnimation
from utils.positionalsound import PositionalSound
from utils.sprite import random_position

MOVE_DAMPING = 0.01
MOVE_CHOICES = [-3000 - 2000, -1000, 0, 1000, 2000, 3000]
HEALTH_EMPTY = 0

AI_INTERVAL = 1 / 2

ANIMATION_IDLE = 'idle.png'
ANIMATION_WALK = 'walk.png'
ANIMATION_DIE = 'die.png'

ANIMATIONS_ALL = {
    ANIMATION_IDLE: AnimationConfig(size=(375, 591), loop=True, frame_length=0.1, apply_modifier=False, reverse=False),
    ANIMATION_WALK: AnimationConfig(size=(389, 592), loop=True, frame_length=0.1, apply_modifier=True, reverse=False),
    ANIMATION_DIE: AnimationConfig(size=(605, 591), loop=False, frame_length=0.1, apply_modifier=True, reverse=False)
}

STATE_IDLE = 'idle'
STATE_WALK = 'walk'
STATE_DEAD = 'dead'
STATE_DEFAULT = STATE_IDLE

WALK_ANIMATION_THRESHOLD = 0.06


class ChickenState:
    def __init__(self, state, value=None):
        self.state = state
        self.value = value

    @property
    def animation(self):
        if self.state == STATE_WALK:
            return ANIMATION_WALK
        if self.state == STATE_DEAD:
            return ANIMATION_DIE

        return ANIMATION_IDLE


class Chicken(Character, Useable):
    def __init__(
            self,
            filename: str = None,
            center_x=0,
            center_y=0
    ):
        super().__init__(filename, center_x=center_x, center_y=center_y)

        self.textures = arcade.load_texture_pair(filename)
        default_face = random.choice([FACE_LEFT, FACE_RIGHT])
        self.face = default_face
        self.texture = self.textures[self.face - 1]
        self.initialized = False
        self.health = HEALTH_FULL
        self._died = False
        self.animations = {}
        self.damping = MOVE_DAMPING
        self.sound = None

        self._state = None
        self._current_animation = None

        self._old_position = None

    def draw_overlay(self, args: ArgsContainer):
        self.draw_healthbar(HEALTHBAR_FREN_COLOR)

    def setup(self, args):
        self._state = ChickenState(state=STATE_DEFAULT)
        self._current_animation = self._state.animation
        self.initialized = True

        for anim in ANIMATIONS_ALL:
            animation = CharacterAnimation()
            config = ANIMATIONS_ALL[anim]
            resize = (32, 50)

            if anim == ANIMATION_DIE:
                resize = (51, 50)
            animation.load(
                state=args.state,
                filename=anim,
                size=config.size,
                loop=config.loop,
                frame_length=config.frame_length,
                apply_modifier=config.apply_modifier,
                character='chicken',
                resize=resize,
                reverse=config.reverse
            )
            self.animations[anim] = animation

        pyglet.clock.schedule_interval_soft(self.ai, AI_INTERVAL, args)

        self._old_position = self.position

    def update(
            self,
            delta_time: float,
            args: ArgsContainer
    ) -> None:
        if not self.initialized:
            self.setup(args)

        if self._state.state == STATE_WALK and self._state.value:
            args.physics_engine.apply_force(self, self._state.value)
            self._state.value = None
            return

        x1, y1 = self.position
        x2, y2 = self._old_position

        diffx = abs(x1 - x2)
        diffy = abs(y1 - y2)
        if self.dead:
            self._state.state = STATE_DEAD
        elif diffx >= WALK_ANIMATION_THRESHOLD or diffy >= WALK_ANIMATION_THRESHOLD:
            self._state.state = STATE_WALK
        elif self._current_animation == ANIMATION_WALK and self.current_animation.last_frame:
            self._state.state = STATE_IDLE

        self._old_position = self.position

        self._current_animation = self._state.animation

        in_sight = args.scene.check_sprite_in_sight(self, args.player)

        if in_sight and self.current_animation and self.current_animation.update():
            self.textures = self.current_animation.current_frame
            self.texture = self.textures[self.face - 1]

        if self._state.state == STATE_DEAD:
            # Remove sprite from physics engine if it hasn't already removed
            if self.sound:
                self.sound.pause()

            # TODO: Replace with static sprite of the last animation frame
            if self.current_animation.completed:
                sprite = arcade.sprite.Sprite(
                    texture=self.current_animation.current_frame[self.face - 1],
                    center_x=self.center_x,
                    center_y=self.center_y
                )

                from constants.layers import LAYER_GROUND
                args.scene.add_sprite(LAYER_GROUND, sprite)
                self.cleanup()
                self.remove_from_sprite_lists()
                return

        if self.sound and self.sound.playing:
            self.sound.update()
            return

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

    def ai(self, delta_time, args):
        if self._state.state == STATE_IDLE:

            if random.randint(1, 10) == 5:

                # randomize play sound
                x, y = random.choice(MOVE_CHOICES), random.choice(MOVE_CHOICES)

                if x == 0 and y == 0:
                    return

                if x < 0:
                    self.face = FACE_LEFT
                elif x > 0:
                    self.face = FACE_RIGHT

                self._state.state = STATE_WALK
                self._state.value = (x, y)
                return

            if random.randint(1, 10) == 5 and args.scene.check_sprite_in_sight(self, args.player):
                self.play_sound(player=args.player, state=args.state)

    def face_towards_player(self, player):
        if self.right < player.left:
            self.face = FACE_RIGHT
            self.texture = self.textures[self.face - 1]

        elif self.left > player.right:
            self.face = FACE_LEFT
            self.texture = self.textures[self.face - 1]

    def schedule(self):
        pyglet.clock.unschedule(self.ai)


def spawn_chicken(state, map_size, scene, physics_engine):
    rand_x, rand_y = random_position(map_size=map_size)

    chicken = Chicken(
        filename=os.path.join(state.sprite_dir, 'char', 'chicken', 'default.png'),
        center_x=rand_x,
        center_y=rand_y
    )

    try:
        if check_collision_with_layers(scene, chicken):
            return spawn_chicken(state, map_size, scene, physics_engine)
    except AttributeError as e:
        logging.error(e)
        return

    scene.add_sprite(LAYER_NPC, chicken)
    physics_engine.add_sprite(
        chicken,
        moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
        collision_type=COLLISION_CHICKEN
    )
