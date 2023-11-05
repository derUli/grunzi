import json
import logging
import os
import random

import sprites.backdrop
import sprites.detailed
import sprites.fire
import sprites.raccoon
import sprites.wall
from constants.game import LEVEL_1_SIZE
from sprites.apple import Apple
from sprites.door import Door
from sprites.key import Key
from sprites.levelexit import LevelExit
from utils.reflections import get_class

LAYER_GROUND = 0
LAYER_STATIC_OBJECTS = 1
LAYER_ITEMS = 2
LAYER_MAINCHAR = 3


class Level:
    def __init__(self, sprites_dir, image_cache, level_file=None):
        self.layers = []
        self.sprites_dir = sprites_dir
        self.image_cache = image_cache

        self.level_file = level_file
        self.level_file_last_changed = None

    def load(self):
        layers = []
        self.level_file_last_changed = os.path.getmtime(self.level_file)

        with open(self.level_file, 'r') as f:
            leveldata = json.loads(f.read())

        for z in leveldata:
            layer = []

            for y in z:
                row = []

                for x in y:
                    if x:
                        sprite_file = None
                        if 'sprite_file' in x:
                            sprite_file = x['sprite_file']

                        try:
                            klass = get_class(x['sprite_class'])
                            sprite = klass(self.sprites_dir, self.image_cache, sprite_file)

                            if 'walkable' in x:
                                sprite.walkable = bool(x['walkable'])
                            else:
                                sprite.walkable = False

                            if 'id' in x:
                                sprite.id = x['id']

                        except ImportError:
                            sprite = None
                            logging.error('Import ' + x['sprite_class'] + ' failed')

                        row.append(sprite)
                    else:
                        row.append(None)
                layer.append(row)
            layers.append(layer)

        self.layers = layers

    def save(self):
        with open(self.level_file, 'w') as f:
            f.write(json.dumps(self.to_saveable_list(), indent=0))

    def randomize(self):
        # Three layers
        self.layers = [
            self.fill_fallback(sprites.backdrop.Backdrop),  # Backdrop layer
            self.fill_fallback(None),  # Static objects
            self.fill_fallback(None),  # Player character
        ]
        self.layers[LAYER_GROUND] = self.build_wall(self.layers[LAYER_GROUND])
        self.layers[LAYER_STATIC_OBJECTS] = self.decorate_flowers(self.layers[LAYER_STATIC_OBJECTS])

        x_from = 5
        y_from = 10

        x_size = 6
        y_size = 5

        x_to = x_from + x_size
        y_to = y_from + y_size

        # Build wall
        for y in range(y_from, y_to):
            self.layers[LAYER_GROUND][y][x_from] = sprites.wall.Wall(self.sprites_dir, self.image_cache)
            self.layers[LAYER_GROUND][y][x_to] = sprites.wall.Wall(self.sprites_dir, self.image_cache)

        for x in range(x_from, x_to + 1):
            self.layers[LAYER_GROUND][y_from][x] = sprites.wall.Wall(self.sprites_dir, self.image_cache)
            self.layers[LAYER_GROUND][y_to][x] = sprites.wall.Wall(self.sprites_dir, self.image_cache)

        self.layers[LAYER_STATIC_OBJECTS][y_to][x_from + 3] = Door(self.sprites_dir, self.image_cache)
        self.layers[LAYER_STATIC_OBJECTS][y_to][x_from] = sprites.wall.Wall(self.sprites_dir, self.image_cache,
                                                                            'postbox.png')

        self.layers[LAYER_GROUND][y_to][x_from + 3] = sprites.backdrop.Backdrop(self.sprites_dir, self.image_cache,
                                                                                'wall.jpg')

        for x in range(x_to - 1, x_to + 1):
            self.layers[LAYER_STATIC_OBJECTS][y_to + 1][x] = sprites.wall.Wall(self.sprites_dir, self.image_cache,
                                                                               'garbagecan.png')

        self.layers[LAYER_STATIC_OBJECTS][y_from + 3][x_from + 3] = Key(
            self.sprites_dir,
            self.image_cache
        )

        self.layers[LAYER_STATIC_OBJECTS][y_from + 3][x_from + 5] = Apple(
            self.sprites_dir,
            self.image_cache
        )
        self.layers[LAYER_STATIC_OBJECTS][y_from + 4][x_from + 5] = Apple(
            self.sprites_dir,
            self.image_cache
        )

        x_from = 6
        y_from = 11

        x_size = 5
        y_size = 4

        x_to = x_from + x_size
        y_to = y_from + y_size

        # Build wall
        for y in range(y_from, y_to):
            for x in range(x_from, x_to):
                self.layers[LAYER_GROUND][y][x] = sprites.backdrop.Backdrop(self.sprites_dir, self.image_cache,
                                                                            'pebble.jpg')

        self.layers[LAYER_STATIC_OBJECTS][0][5] = sprites.detailed.Detailed(
            self.sprites_dir, self.image_cache, 'dont_waste_water.png')

        self.layers[LAYER_STATIC_OBJECTS][8][0] = sprites.detailed.Detailed(
            self.sprites_dir, self.image_cache, 'sunset.png')

        self.layers[LAYER_STATIC_OBJECTS][3][4] = sprites.detailed.Detailed(
            self.sprites_dir, self.image_cache, 'bubblegum.png')

        self.layers[LAYER_STATIC_OBJECTS][10][20] = Key(
            self.sprites_dir,
            self.image_cache
        )

        raccoon = sprites.raccoon.Raccoon(self.sprites_dir,
                                          self.image_cache)

        self.layers[LAYER_STATIC_OBJECTS][7][8] = raccoon

        for x in [10, 11, 50, 51, 52]:
            self.layers[LAYER_STATIC_OBJECTS][0][x] = sprites.fire.Fire(
                self.sprites_dir,
                self.image_cache
            )

    def purge_sprites(self):
        """ Search character by id """
        for z in range(0, len(self.layers)):
            for y in range(0, len(self.layers[z])):
                for x in range(0, len(self.layers[z][y])):
                    element = self.layers[z][y][x]
                    if element and element.purge:
                        self.layers[z][y][x] = None
        return

    def is_walkable(self, x, y):
        """ Check if a sprite  is walkable"""
        for z in self.layers:
            if not z[y][x]:
                continue

            if not z[y][x].walkable:
                return False

        return True

    def is_levelexit(self, x, y):
        """ Check if a sprite  is walkable"""
        for z in self.layers:
            if not z[y][x]:
                continue

            if isinstance(z[y][x], LevelExit):
                return True

        return False

    def search_character(self, id):
        """ Search character by id """
        for z in range(0, len(self.layers)):
            for y in range(0, len(self.layers[z])):
                for x in range(0, len(self.layers[z][y])):
                    element = self.layers[z][y][x]
                    if element and element.id == id:
                        return (z, y, x)

        return (0, 0, 0)

    def search_sprite(self, sprite):
        """ Search character by id """
        for z in range(0, len(self.layers)):
            for y in range(0, len(self.layers[z])):
                for x in range(0, len(self.layers[z][y])):
                    if self.layers[z][y][x] == sprite:
                        return (z, y, x)

        return (0, 0, 0)

    def move_sprite(self, sprite, target_pos):
        old_z, old_y, old_x = self.search_sprite(sprite)
        z, y, x = target_pos

        if self.layers[z][y][x]:
            return False

        self.layers[old_z][old_y][old_x] = None
        self.layers[z][y][x] = sprite


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

    def to_saveable_list(self):
        layers = []

        for z in self.layers:
            layer = []

            for y in z:
                row = []

                for x in y:
                    if x:
                        row.append(x.to_dict())
                    else:
                        row.append(0)

                layer.append(row)
            layers.append(layer)

        return layers

    def check_for_changes(self):
        """ Check for changes """
        changed = False
        if not self.level_file:
            return changed

        if os.path.getmtime(self.level_file) != self.level_file_last_changed:
            logging.debug('Map file changed ' + self.level_file)
            changed = True

        return changed
