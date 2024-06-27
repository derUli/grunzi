from typing import Optional

from arcade import Texture

from sprites.sprite import Sprite
from state.argscontainer import ArgsContainer
from utils.positionalsound import PositionalSound, VOLUME_SOURCE_ATMO


class Highway(Sprite):
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
            angle: float = 0,
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
