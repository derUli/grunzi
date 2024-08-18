from typing import Optional

from arcade import Texture
from arcade.types import PathOrTexture

from sprites.sprite import Sprite
from state.argscontainer import ArgsContainer
from utils.positionalsound import PositionalSound, VOLUME_SOURCE_ATMO


class Highway(Sprite):
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
        self.sound = None

    def update(
            self,
            delta_time: float,
            args: ArgsContainer
    ) -> None:
        """
        Update beach sound
        @param delta_time: Delta time
        @param args: ArgsContainer
        """
        if not self.sound:
            audio = args.state.play_sound('atmos', 'highway', loop=True)
            self.sound = PositionalSound(
                args.player,
                self,
                audio,
                args.state,
                volume_source=VOLUME_SOURCE_ATMO
            )

        self.sound.update()
