import sprites.backdrop
import sprites.fire
import sprites.wall
import sprites.raccoon
import sprites.detailed
import random
from constants.game import LEVEL_1_SIZE

LAYER_GROUND = 0
LAYER_STATIC_OBJECTS = 1
LAYER_MAINCHAR = 2

class Level:
    def __init__(self, sprites_dir, image_cache):
        self.layers = []
        self.sprites_dir = sprites_dir
        self.image_cache = image_cache

    def fill_layers(self):
        # Three layers
        self.layers = [
            self.fill_fallback(sprites.backdrop.Backdrop),  # Backdrop layer
            self.fill_fallback(None),  # Static objects
            self.fill_fallback(None),  # Player character
        ]

        self.layers[LAYER_GROUND] = self.build_wall(self.layers[LAYER_GROUND])

        self.layers[LAYER_STATIC_OBJECTS][0][5] = sprites.detailed.Detailed(
            self.sprites_dir, self.image_cache, 'dont_waste_water.png')

        self.layers[LAYER_STATIC_OBJECTS][8][0] = sprites.detailed.Detailed(
            self.sprites_dir, self.image_cache, 'sunset.png')

        self.layers[LAYER_STATIC_OBJECTS][3][4] = sprites.detailed.Detailed(
            self.sprites_dir, self.image_cache, 'bubblegum.png')

        self.camera_offset = (5, 3)

        raccoon = sprites.raccoon.Raccoon(self.sprites_dir,
                                          self.image_cache)

        self.layers[LAYER_STATIC_OBJECTS][7][8] = raccoon

        self.layers[LAYER_STATIC_OBJECTS][0][10] = sprites.fire.Fire(
            self.sprites_dir,
            self.image_cache
        )

        self.layers[LAYER_STATIC_OBJECTS][0][11] = sprites.fire.Fire(
            self.sprites_dir,
            self.image_cache
        )

        self.layers[LAYER_STATIC_OBJECTS] = self.decorate_flowers(self.layers[LAYER_STATIC_OBJECTS])

    def search_character(self, id):
        """ Search character by id """
        for z in range(0, len(self.layers)):
            for y in range(0, len(self.layers[z])):
                for x in range(0, len(self.layers[z][y])):
                    element = self.layers[z][y][x]
                    if element and element.id == id:
                        return (z, y, x)

        return (0, 0, 0)

    def fill_fallback(self, callable):
        max_x, max_y = LEVEL_1_SIZE

        rows = []

        for i in range(0, max_y):
            cols = []

            for n in range(0, max_x):
                s = None
                if callable:
                    s = callable(self.sprites_dir, self.image_cache)
                cols.append(s)

            rows.append(cols)

        return rows

    def build_wall(self, layer):

        for y in range(0, len(layer)):
            for x in range(0, len(layer[y])):
                is_wall = False
                if y == 0 or y == len(layer) - 1:
                    is_wall = True

                if x == 0 or x == len(layer[y]) - 1:
                    is_wall = True

                if is_wall:
                    layer[y][x] = sprites.wall.Wall(
                        self.sprites_dir, self.image_cache)

        return layer

    def decorate_flowers(self, layer):
        flowers = [
            'flower1.png',
            'flower2.png',
            'flower3.png',
            'flower4.png',
            'flower5.png'
        ]
        for y in range(0, len(layer)):
            for x in range(0, len(layer[y])):

                layers_count = len(self.layers)

                walkable = True
                for z in range(0, layers_count):
                    if self.layers[z][y][x]:
                        if not self.layers[z][y][x].walkable:
                            walkable = False
                place_flower = random.randint(1, 10) == 2

                if walkable and place_flower:
                    layer[y][x] = sprites.backdrop.Backdrop(
                        self.sprites_dir, self.image_cache, random.choice(
                            flowers)
                    )

        return layer
