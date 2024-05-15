import random

import arcade
from arcade import FACE_RIGHT, FACE_LEFT

from sprites.characters.character import Character
from sprites.characters.spritehealth import HEALTH_FULL, HEALTHBAR_FREN_COLOR
from sprites.items.item import Useable
from utils.positional_sound import PositionalSound

FADE_SPEED = 4
DEFAULT_FACE = FACE_RIGHT
MOVE_DAMPING = 0.01
MOVE_FORCE = 2000


class Duck(Character, Useable):
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

        self.textures = arcade.load_texture_pair(filename)
        self.face = random.choice([FACE_LEFT, FACE_RIGHT])
        self.face_horizontal = self.face
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
            delta_time,
            args
    ):
        # randomize play sound
        if random.randint(1, 50) == 30:
            self.play_sound(player=args.player, state=args.state)

        if self.sound:
            self.sound.update()

    def play_sound(self, player, state):
        if self.sound and self.sound.playing:
            return

        audio = state.play_sound('duck' + str(random.randint(1, 3)), volume=0)
        self.sound = PositionalSound(player, self, audio, state)
        self.sound.play()
