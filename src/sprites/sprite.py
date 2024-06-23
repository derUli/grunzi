""" Sprite classes """

from typing import Optional

import arcade.sprite
from arcade import Texture

FADE_SPEED = 255 / 20


class AbstractSprite:
    def draw_overlay(self, args):
        """ Draw overlay """
        pass

    def update(
            self,
            delta_time,
            args
    ):
        pass


class AbstractStaticSprite(AbstractSprite, arcade.sprite.Sprite):
    """ Abstract sprite class """
    pass


class AbstractAnimatedSprite(AbstractSprite, arcade.sprite.AnimatedTimeBasedSprite):
    """ Abstract animated sprite class """

    def __init__(
            self,
            filename: Optional[str] = None,
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
        self.sound = None

        super().__init__(
            filename=filename,
            image_x=image_x,
            image_y=image_y,
        )


class Sprite(AbstractStaticSprite):
    def __init__(
            self,
            filename: str = None,
            scale: float = 1,
            image_x: float = 0,
            image_y: float = 0,
            image_width: float = 0,
            image_height: float = 0,
            center_x: float = 0,
            center_y: float = 0,
            repeat_count_x: int = 1,  # Unused
            repeat_count_y: int = 1,  # Unused
            flipped_horizontally: bool = False,
            flipped_vertically: bool = False,
            flipped_diagonally: bool = False,
            hit_box_algorithm: Optional[str] = "Simple",
            hit_box_detail: float = 4.5,
            texture: Texture = None,
            angle: float = 0
    ):
        super().__init__(
            filename,
            scale,
            image_x,
            image_y,
            image_width,
            image_height,
            center_x,
            center_y,
            flipped_horizontally,
            flipped_vertically,
            flipped_diagonally,
            hit_box_algorithm,
            hit_box_detail,
            texture,
            angle,
        )

        self.insight = False
        self.fadeout = False

    def update(
            self,
            delta_time,
            args
    ):
        if self.fadeout:
            alpha = self.alpha - FADE_SPEED

            if alpha <= 0:
                alpha = 0
                self.remove_from_sprite_lists()

            self.alpha = alpha

    def fade_destroy(self) -> bool:
        """ Fade out and destroy """

        if not self.fadeout:
            self.fadeout = True
            return True

        return False
