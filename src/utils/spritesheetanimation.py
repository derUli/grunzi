import os

from PIL import Image
from PIL.Image import Resampling


class SpriteSheetReader:
    def __init__(self, filename):
        self._filename = filename
        self._images = []

    def process(self, size, autocrop=False, resize=None):
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
                        resample=Resampling.BILINEAR
                    )

                self._images.append(cropped)

                x += w

            y += h

    @property
    def images(self):
        return self._images