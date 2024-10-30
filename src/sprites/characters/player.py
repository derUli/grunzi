""" Player sprite class """
import math

import arcade
import pyglet.clock
from arcade import FACE_RIGHT, FACE_LEFT, FACE_DOWN, FACE_UP

from constants.layers import LAYER_SPAWN_POINT, LAYER_PLAYER, LAYER_LEVEL_EXIT
from sprites.characters.character import Character
from sprites.characters.spritehealth import HEALTH_FULL, SpriteHealth, HEALTH_EMPTY
from sprites.ui.bloodyscreen import BloodyScreen
from sprites.ui.gameovertext import GameOverText
from utils.animationconfig import AnimationConfig
from utils.characteranimation import CharacterAnimation

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
MOVE_FORCE = 2400

MODIFIER_DEFAULT = 1
MODIFIER_SPRINT = 1.7

MOVE_DAMPING = 0.01

PLACE_ITEM_ALPHA = 255

INVENTORY_MARGIN = 15

SPAWN_POINT = (0, 0)

DEFAULT_BULLET_SIZE = 10
BULLET_DECREMENTOR = 0.4

ANIMATION_IDLE = '__pig_idle.png'
ANIMATION_WALKING = '__pig_walk_run.png'
ANIMATION_GRUNT = '__pig_jump.png'
ANIMATION_DIE = '__pig_die.png'

ANIMATIONS_ALL = {
    ANIMATION_IDLE: AnimationConfig(size=(424.2, 227), loop=True, frame_length=0.2, apply_modifier=False),
    ANIMATION_WALKING: AnimationConfig(size=(360, 194), loop=True, frame_length=0.08, apply_modifier=True),
    ANIMATION_GRUNT: AnimationConfig(size=(414.6, 268), loop=False, frame_length=0.005, apply_modifier=False),
    ANIMATION_DIE: AnimationConfig(size=(404.4, 252), loop=False, frame_length=0.1, apply_modifier=False)
}


class Player(Character, SpriteHealth):
    def __init__(
            self,
            filename: str = None,
    ):
        super().__init__()

        self.move_force = MOVE_FORCE
        self.modifier = MODIFIER_DEFAULT
        self.damping = MOVE_DAMPING
        self.textures = arcade.load_texture_pair(filename)

        self.health = HEALTH_FULL
        self.face = DEFAULT_FACE
        self.face_horizontal = DEFAULT_FACE
        self.texture = self.textures[self.face - 1]

        self.item = None

        self.state = None
        self.water = False
        self._died = False

        self.footsteps_default = None
        self.footsteps_sprint = None

        self.gameover_text = None

        self._bullet_size = DEFAULT_BULLET_SIZE

        self.bloody_screen = None
        self.walking = False
        self.controllers = []
        self.initialized = False
        self.animations = {}
        self._current_animation = ANIMATION_IDLE

    def setup(self, state, scene, callbacks, controllers, bullet_size):
        self.state = state
        self.scene = scene
        self.callbacks = callbacks
        self.controllers = controllers
        self.bullet_size = bullet_size

        self.center_x, self.center_y = SPAWN_POINT

        if LAYER_SPAWN_POINT not in self.scene.name_mapping:
            return

        for sprite in self.scene.get_sprite_list(LAYER_SPAWN_POINT):
            self.center_x, self.center_y = sprite.center_x, sprite.center_y
            sprite.remove_from_sprite_lists()

        scene.add_sprite(LAYER_PLAYER, self)

        self.footsteps_default = state.play_sound('footsteps', loop=True, speed=MODIFIER_DEFAULT)
        self.footsteps_default.pause()

        self.footsteps_sprint = state.play_sound('footsteps', loop=True, speed=MODIFIER_SPRINT)
        self.footsteps_sprint.pause()

        self.bloody_screen = BloodyScreen().setup(state)

        self.initialized = False

        for anim in ANIMATIONS_ALL:
            animation = CharacterAnimation()
            config = ANIMATIONS_ALL[anim]
            animation.load(
                state=state,
                filename=anim,
                size=config.size,
                loop=config.loop,
                frame_length=config.frame_length,
                apply_modifier=config.apply_modifier,
                resize=(70, 39),
                character='pig'
            )
            self.animations[anim] = animation

        self.current_animation = ANIMATION_IDLE

        self.textures = self.animations[ANIMATION_IDLE].current_frame
        self.update_texture()

    def update_texture(self):
        self.texture = self.textures[self.face_horizontal - 1]

    def reset(self):
        self.modifier = MODIFIER_DEFAULT
        self.stop_walk()

    def update(
            self,
            delta_time,
            args
    ):

        if not self.initialized:
            pyglet.clock.schedule_interval_soft(self.check_for_levelexit, 1 / 5, args)
            self.initialized = True

        if self.health <= HEALTH_EMPTY and self._current_animation != ANIMATION_DIE:
            if self._current_animation != ANIMATION_DIE:
                self.current_animation = ANIMATION_DIE

        self.bloody_screen.update(self.health)

        if self.dead:
            return

        if self.health < HEALTH_FULL:
            self.health += args.state.difficulty.health_regeneration_speed

        if self.health > HEALTH_FULL:
            self.health = HEALTH_FULL

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.set_face(FACE_LEFT)
        elif self.change_x > 0:
            self.set_face(FACE_RIGHT)
        elif self.change_y > 0:
            self.set_face(FACE_DOWN)
        elif self.change_y < 0:
            self.set_face(FACE_UP)

        if self.item:
            if self.face == FACE_RIGHT:
                self.item.left = self.right + INVENTORY_MARGIN
                self.item.center_y = self.center_y
            elif self.face == FACE_LEFT:
                self.item.right = self.left - INVENTORY_MARGIN
                self.item.center_y = self.center_y
            elif self.face == FACE_UP:
                self.item.center_x = self.center_x
                bottom = self.top + INVENTORY_MARGIN

                if self.item.height > self.item.width:
                    bottom += INVENTORY_MARGIN

                self.item.bottom = bottom

            elif self.face == FACE_DOWN:
                self.item.center_x = self.center_x
                top = self.bottom - INVENTORY_MARGIN

                if self.item.height > self.item.width:
                    top -= INVENTORY_MARGIN

                self.item.top = top

            self.item.alpha = PLACE_ITEM_ALPHA
            self.item.draw_item(self.face)

    def update_animation(self):

        if self.current_animation:
            if self.current_animation.completed:
                if self.health <= HEALTH_EMPTY:
                    return

                self.current_animation = ANIMATION_IDLE
                return

            if self.current_animation.update(self.modifier):
                self.textures = self.current_animation.current_frame
                self.update_texture()

    def draw_overlay(self, args):
        self.bloody_screen.draw()

        if not self.dead:
            return

        if not self.gameover_text:
            self.gameover_text = GameOverText()
            self.gameover_text.setup()

        self.gameover_text.draw()

    def set_item(self, item):
        if self.item:
            self.item.alpha = 0

            if item is None:
                self.item.remove_from_sprite_lists()

        self.item = item
        return item

    def get_item(self):
        return self.item

    def set_face(self, face):
        if face in [FACE_LEFT, FACE_RIGHT]:
            self.face_horizontal = face
            self.update_texture()

        self.face = face

    def hurt(self, damage: int | float) -> None:
        """
        Hurt player
        @param damage: Damage amount to apply
        """

        for controller in self.controllers:
            if not self.state.settings.vibration:
                break

            controller.rumble_play_weak()

        super().hurt(damage)

    def on_die(self) -> None:
        """ Called when the player dies """

        self.state.squeak()
        self.scene.cleanup()

    def on_grunt(self):
        self.current_animation = ANIMATION_GRUNT

    def start_walk(self, sprint=False):
        self.walking = True

        self.current_animation = ANIMATION_WALKING

        volume = 1
        self.footsteps_default.volume = volume * self.state.settings.sound_volume * self.state.settings.master_volume
        self.footsteps_sprint.volume = volume * self.state.settings.sound_volume * self.state.settings.master_volume

        if sprint:

            if self.footsteps_default.playing:
                self.footsteps_default.pause()

            if not self.footsteps_sprint.playing:
                self.footsteps_sprint.play()
                return

        if self.footsteps_sprint.playing:
            self.footsteps_sprint.pause()

        if not self.footsteps_default.playing:
            self.footsteps_default.play()

    def stop_walk(self):
        if not self.walking:
            return

        self.walking = False
        self.current_animation = ANIMATION_IDLE
        self.footsteps_default.pause()
        self.footsteps_sprint.pause()

    @property
    def sprinting(self):
        return self.modifier == MODIFIER_SPRINT

    def shoot(self, state, scene, physics_engine):

        from sprites.bullet.bullet import Bullet

        hurt_modifier = (self.bullet_size / DEFAULT_BULLET_SIZE)
        Bullet(
            int(math.ceil(self.bullet_size)),
            color=arcade.csscolor.HOTPINK,
            hurt_modifier=hurt_modifier
        ).setup(
            source=self,
            physics_engine=physics_engine,
            state=state,
            scene=scene
        )

        self.bullet_size -= BULLET_DECREMENTOR

    @property
    def bullet_size(self) -> int:
        return self._bullet_size

    @bullet_size.setter
    def bullet_size(self, value: int):
        if value < DEFAULT_BULLET_SIZE:
            value = DEFAULT_BULLET_SIZE

        self._bullet_size = value

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

    def check_for_levelexit(self, delta_time, args):

        try:
            exit_layer = args.scene[LAYER_LEVEL_EXIT]
        except KeyError:
            # Unschedule if there is no level exit trigger
            self.cleanup()
            return

        if any(arcade.check_for_collision_with_list(self, exit_layer)):
            args.callbacks.on_complete()
            return

    def cleanup(self):
        pyglet.clock.unschedule(self.check_for_levelexit)
