""" Wall sprite """
from sprites.takeable import Takeable
from stopwatch import Stopwatch
from utils.audio import play_sound
from utils.animation import Animation
from constants.graphics import SPRITE_SIZE
from utils.quality import font_antialiasing_enabled
from constants.game import MONOTYPE_FONT, MAIN_CHARACTER_ID
import os
import pygame

COUNT_TO = 3

TARGET_POS_X = 48
TARGET_POS_Y = 148

DAMAGE_ZONE = 2


class Dynamite(Takeable):
    """ Wall sprite class """

    def __init__(self, sprite_dir, cache, sprite='dynamite.png'):
        """ Constructor """
        super().__init__(sprite_dir, cache, sprite)

        self.clock = Stopwatch()
        self.clock.stop()
        self.last_second = 0

        animation_dir = os.path.join(sprite_dir, 'animations', 'explosion')

        data_dir = os.path.abspath(
            os.path.join(
                self.sprite_dir,
                '..',
                ' ..',
                '..',
                '..'))

        self.exploded = False

        self.explosion = Animation(
            animation_dir,
            refresh_interval=0.08,
            start_frame=0,
            size=SPRITE_SIZE,
            loop=False
        )

        self.monotype_font = pygame.font.Font(
            os.path.join(data_dir, 'fonts', MONOTYPE_FONT),
            6
        )

    def start_counter(self):
        self.last_second = 0
        self.clock.reset()
        self.clock.start()
        self.walkable = False

    def draw(self, screen, x, y):
        timer_text = ''

        if self.clock.running:
            timer_text = str(COUNT_TO - self.last_second)

        timer_color = (0, 0, 255)

        pos = self.calculate_pos(x, y)

        if not self.exploded:
            super().draw(screen, x, y)

            rendered_text = self.monotype_font.render(
                timer_text,
                font_antialiasing_enabled(),
                pygame.Color(timer_color)
            )

            text_pos_x, text_pos_y = pos

            text_pos_y += 29
            text_pos_x += 32

            screen.blit(rendered_text, (text_pos_x, text_pos_y))

            return

        frame = self.explosion.get_frame()

        screen.blit(frame, pos)

        if not self.explosion.has_more_frames():
            self.purge = True

    def ai(self, level):
        z, y, x = level.search_sprite(self)

        mc_z, mc_y, mc_x = level.search_by_id(MAIN_CHARACTER_ID)
        mainchar = level.layers[mc_z][mc_y][mc_x]

        if self.exploded:

            if mainchar and mc_y == y:
                diff_x = x - mc_x

                if diff_x <= DAMAGE_ZONE:

                    damage_amount = 1

                    if diff_x <= 1:
                        damage_amount = 20

                    if mainchar:
                        mainchar.state.hurt(damage_amount)

            mw_z, mw_y, mw_x = level.search_by_id('microwave')
            microwave = level.layers[mw_z][mw_y][mw_x]
            if microwave:
                microwave.explode = True
            return

        if y == TARGET_POS_Y and x == TARGET_POS_X and not self.clock.running:
            self.start_counter()
            mainchar.state.say(_('Allahu Akbar!'))
            return

        second = int(self.clock.duration)

        if second > self.last_second and not self.exploded:
            self.last_second = second
            self.play_countdown_sound()

        if second >= COUNT_TO:
            self.clock.stop()
            self.play_explosion_sound()
            self.exploded = True

    def play_countdown_sound(self):
        play_sound(
            os.path.join(
                self.sprite_dir,
                '..',
                '..',
                'sounds',
                'common',
                'countdown.ogg'
            )
        )

    def play_explosion_sound(self):
        play_sound(
            os.path.join(
                self.sprite_dir,
                '..',
                '..',
                'sounds',
                'common',
                'explosion.ogg'
            )
        )
