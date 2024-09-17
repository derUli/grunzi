""" Slimer sprite class """
import os
import random

import PIL
import arcade
import pyglet.clock
from arcade import FACE_RIGHT, PymunkPhysicsEngine

from constants.collisions import COLLISION_ENEMY
from sprites.characters.character import Character
from utils.positionalsound import PositionalSound, VOLUME_SOURCE_SOUND
from window.gamewindow import UPDATE_RATE

DEFAULT_FACE = FACE_RIGHT

# Physics stuff
FORCE_MOVE = 200000

EYE_OFFSET_X = 100
EYE_SPACING_X = 250
EYE_OFFSET_Y = 10

ALPHA_SPEED = 2
ALPHA_MAX = 255


class Boss(Character):
    def __init__(
            self,
            filename: str | None = None,
            image_x=0,
            image_y=0,
            image_width=None,
            image_height=None,
            flipped_horizontally=False,
            flipped_vertically=False,
            flipped_diagonally=False,
            hit_box_algorithm=None,
            hit_box_detail=None,
            scale=1.0,
            center_x=None,
            center_y=None
    ):
        super().__init__(filename, center_x=center_x, center_y=center_y)

        self.eye_file = os.path.join(os.path.dirname(filename), 'eye.png')
        self.laser_file = os.path.join(os.path.dirname(filename), 'laser.jpg')
        self.eye1 = None
        self.eye2 = None
        self.spawn_sound = None
        self.triggered = False
        self.lasers = []
        self.fighting = False
        self.force = random.choice([FORCE_MOVE, FORCE_MOVE * -1])
        self._should_shoot = False
        self.laser_sound = None
        self.initial_music_volume = None
        self.settings = None

    def update(self, delta_time, args):

        from constants.layers import LAYER_CRYSTAL

        super().update(delta_time, args)

        crystal_count = len(args.scene[LAYER_CRYSTAL])

        min_health = crystal_count * 10

        if self.health < min_health:
            self.health = min_health

        self.eye1.center_x = self.center_x - EYE_OFFSET_X
        self.eye1.center_y = self.center_y - EYE_OFFSET_Y
        self.eye1.alpha = self.alpha

        self.eye2.center_x = self.eye1.center_x + EYE_SPACING_X
        self.eye2.center_y = self.eye1.center_y
        self.eye2.alpha = self.alpha

        if self.laser_sound:
            self.laser_sound.update(max_distance=args.tilemap.width)

        if self.dead:

            if self.laser_sound:
                self.laser_sound.pause()
                self.laser_sound = None

            for laser in self.lasers:
                laser.remove_from_sprite_lists()

            # Fade out on death
            if self.fade_destroy():
                self.cleanup()

                self.fadeout_volume(0, args)

            return

        if not self.triggered:
            return

        if self.alpha < ALPHA_MAX:
            alpha = self.alpha + ALPHA_SPEED

            if alpha > ALPHA_MAX:
                alpha = ALPHA_MAX

            self.alpha = alpha

        if not self.spawn_sound.playing and not self.fighting:
            self.fighting = True
            pyglet.clock.schedule_once(
                self.should_shoot,
                random.randint(1, args.state.difficulty.boss_range),
                args
            )
            pyglet.clock.schedule_interval_soft(self.collision_lasers, 1 / 72, args)

        if not self.fighting:
            return

        if self.force > 0 and args.player.center_y < self.center_y:
            self.force *= -1
        elif self.force < 0 and args.player.center_y > self.center_y:
            self.force *= -1

        args.physics_engine.apply_force(self, (0, self.force))

        self.update_laser(args)

    def update_laser(self, args):
        if not self._should_shoot:
            return

        laser_index = 0

        i = 0
        for laser in self.lasers:

            if laser.visible:
                laser_index = i
                break
            i += 1

        self.lasers[laser_index].visible = False

        if laser_index + 1 < len(self.lasers):
            next_laser = self.lasers[laser_index + 1]
            next_laser.visible = True
            if args.player.left > self.center_x:
                next_laser.left = self.eye2.right
            else:
                next_laser.right = self.eye1.left

            next_laser.center_y = self.eye1.center_y
        else:
            self.lasers[laser_index].visible = False
            self.lasers[0].visible = True
            self._should_shoot = False

            self.laser_sound.pause()

    def setup(self, args):
        pyglet.clock.schedule_interval_soft(self.check_trigger, 1 / 6, args)
        self.settings = args.state.settings
        self.initial_music_volume = args.state.settings.music_volume

        self.setup_boss(args)
        self.setup_eyes(args)
        self.setup_laser(args)

    def setup_boss(self, args):

        self.alpha = 0
        from constants.layers import LAYER_NPC

        self.remove_from_sprite_lists()

        args.scene.add_sprite(LAYER_NPC, self)

        args.physics_engine.add_sprite(
            self,
            mass=500,
            moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
            collision_type=COLLISION_ENEMY
        )

    def setup_eyes(self, args):
        from constants.layers import LAYER_NPC

        self.eye1 = arcade.sprite.Sprite(filename=self.eye_file)
        args.scene.add_sprite(LAYER_NPC, self.eye1)

        self.eye2 = arcade.sprite.Sprite(filename=self.eye_file, flipped_horizontally=True)
        args.scene.add_sprite(LAYER_NPC, self.eye2)

    def collision_lasers(self, delta_time, args):

        visible = list(filter(lambda x: x.visible, self.lasers))

        if not any(visible):
            return

        if arcade.check_for_collision(visible[0], args.player):
            args.player.hurt(args.state.difficulty.boss_laser_hurt)

    def setup_laser(self, args):
        from constants.layers import LAYER_NPC

        self.lasers = []

        laser_image = PIL.Image.open(
            self.laser_file
        ).convert('RGBA')

        laser_image = laser_image.resize((laser_image.width * 3, laser_image.height * 2))

        laser_range = []

        for i in range(1, int(UPDATE_RATE * laser_image.width)):
            laser_range.append(i * 72)

        for i in laser_range:
            image = laser_image.crop((0, 0, i, laser_image.height))
            texture = arcade.texture.Texture(image=image, name=f"laser-{i}")
            sprite = arcade.sprite.Sprite(texture=texture)
            sprite.visible = False
            self.lasers.append(sprite)
            args.scene.add_sprite(LAYER_NPC, sprite)

    def draw_overlay(self, args):
        self.draw_healthbar()

    def should_shoot(self, delta_time, args):

        if not self._should_shoot:
            self._should_shoot = True
            self.lasers[0].visible = True

            if not self.laser_sound:
                audio = args.state.play_sound('boss', 'laser', loop=True)

                self.laser_sound = PositionalSound(
                    args.player,
                    self,
                    audio,
                    args.state,
                    volume_source=VOLUME_SOURCE_SOUND
                )

            self.laser_sound.play()

        pyglet.clock.schedule_once(
            self.should_shoot,
            random.randint(1, args.state.difficulty.boss_range),
            args
        )

    def cleanup(self):
        self.settings.music_volume = self.initial_music_volume

        pyglet.clock.unschedule(self.should_shoot)
        pyglet.clock.unschedule(self.collision_lasers)
        pyglet.clock.unschedule(self.check_trigger)

    def check_trigger(self, delta_time, args):
        collides = False
        from constants.layers import LAYER_BOSS_TRIGGER

        for sprite in args.scene[LAYER_BOSS_TRIGGER]:
            if arcade.get_distance_between_sprites(sprite, args.player) <= 100:
                collides = True
                break

        if not collides:
            return

        self.triggered = True

        args.music_queue.reset()
        args.music_queue.from_directory(os.path.join(args.state.music_dir, 'map05b'))
        args.music_queue.next()

        self.spawn_sound = args.state.play_sound('boss', 'spawn')

        pyglet.clock.unschedule(self.check_trigger)

    def fadeout_volume(self, delta_time, args):

        music_volume = args.state.settings.music_volume - 0.01

        if music_volume < 0:
            music_volume = 0

        args.state.settings.music_volume = music_volume

        if music_volume <= 0:
            args.music_queue.reset()

            args.state.settings.music_volume = self.initial_music_volume * args.settings.master_volume
            return

        pyglet.clock.schedule_once(self.fadeout_volume, 1 / 25, args)
