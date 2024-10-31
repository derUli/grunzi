""" Reads a spritesheet from image """

from PIL import Image
from PIL.Image import Resampling


class SpriteSheetReader:
    """ Reads a spritesheet from image """

    def __init__(self, filename):
        """
        Constructor
        @param filename: The image filename
        """
        self._filename = filename
        self._images = []

    def process(
            self,
            size: float,
            autocrop: bool = False,
            resize: tuple | None = None,
            reverse: bool = False,
            pil_resample: int = Resampling.BILINEAR) -> list:
        """
        Processes a spritesheet
        @param size: Size of the spritesheet images
        @param autocrop: Autocrop the images
        @param resize: Resize all images to this size
        @param pil_resample: PIL Resampling algorithm

        @return: List of PIL images
        """

        self._images = []

        image = Image.open(self._filename).convert('RGBA').crop()

        full_w, full_h = image.size

        w, h = size

        y = 0

        while y < full_h:
            x = 0

            while x < full_w:
                img_area = (x, y, x + w, y + h)
                cropped = image.crop(img_area)

                if autocrop:
                    cropped = cropped.crop()

                if resize:
                    cropped = cropped.resize(
                        resize,
                        resample=pil_resample
                    )

                self._images.append(cropped)

                x += w

            y += h

        if reverse:
            self._images = list(reversed(self._images))

        return self.images

    @property
    def images(self):
        """ Return list of images """

        return self._images
