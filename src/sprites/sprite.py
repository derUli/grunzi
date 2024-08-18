""" Sprite classes """

from typing import Optional

import arcade.sprite
from arcade import Texture
from arcade.types import PathOrTexture

from state.argscontainer import ArgsContainer

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

    def setup(self, args):
        pass


class AbstractStaticSprite(AbstractSprite, arcade.sprite.Sprite):
    """ Abstract sprite class """
    pass


class AbstractAnimatedSprite(AbstractSprite, arcade.sprite.animated.TextureAnimationSprite):
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
            path_or_texture: PathOrTexture | None = None,
            scale: float = 1.0,
            center_x: float = 0.0,
            center_y: float = 0.0,
            angle: float = 0.0,
    ):
        super().__init__(
            path_or_texture,
            scale,
            center_x,
            center_y,
            angle
        )

        self.insight = False
        self.fadeout = False
        self.attributes = {}

    def update(
            self,
            delta_time: float,
            args: ArgsContainer
    ) -> None:
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


class AlphaWall(Sprite):
    def setup(self, args):
        self.alpha = 0
