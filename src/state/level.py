import json
import logging
import os
import random
import time

import pygame

import constants.graphics
import sprites.backdrop
import sprites.detailed
import sprites.fire
import sprites.raccoon
import sprites.wall
from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_UP
from constants.game import LEVEL_1_SIZE
from sprites.apple import Apple
from sprites.door import Door
from sprites.key import Key
from sprites.levelexit import LevelExit
from utils.reflections import get_class
from utils.screenshot import make_dump

LAYER_GROUND = 0
LAYER_STATIC_OBJECTS = 1
LAYER_ITEMS = 2
LAYER_OTHER_CHARS = 3
LAYER_MAINCHAR = 4


class Level:
    def __init__(self, sprites_dir, image_cache, level_file=None):
        self.layers = []
        self.sprites_dir = sprites_dir
        self.image_cache = image_cache
        self.loaded = False
        self.level_file = level_file
        self.level_file_last_changed = None

    def load(self, progress_callback = None):
        self.loaded = False
        load_start = time.time()
        layers = []
        self.level_file_last_changed = os.path.getmtime(self.level_file)

        with open(self.level_file, 'r') as f:
            leveldata = json.loads(f.read())

        total_blocks = 0
        for z in leveldata:
            for y in z:
                for x in y:
                    total_blocks += 1

        one_percent = 100 / total_blocks

        loaded_percent = 0
        loaded_blocks = 0

        if progress_callback:
            progress_callback(loaded_percent)

        for z in leveldata:
            layer = []

            for y in z:
                row = []

                for x in y:
                    loaded_blocks += 1
                    percentage = round(one_percent * loaded_blocks)

                    if percentage != loaded_percent:
                        loaded_percent = percentage

                        if progress_callback:
                            progress_callback(loaded_percent)

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
        self.loaded = True

        load_end = time.time()
        load_time = load_end - load_start
        logging.debug("Loading time: " + str(load_time))

    def save(self):
        with open(self.level_file, 'w') as f:
            f.write(json.dumps(self.to_saveable_list(), indent=0))

    def dump(self):
        w, h = constants.graphics.SPRITE_SIZE

        total_w = len(self.layers[0][0]) * w
        total_h = len(self.layers[0]) * h

        surface = pygame.surface.Surface((total_w, total_h))

        for z in range(0, len(self.layers)):
            for y in range(0, len(self.layers[z])):
                for x in range(0, len(self.layers[z][y])):
                    element = self.layers[z][y][x]
                    if element:
                        if hasattr(element, 'animation'):
                            # Wait for animation frame loading
                            while len(element.animation.frames) == 0:
                                element.draw(surface, x, y)

                        else:
                            element.draw(surface, x, y)

        make_dump(surface)

    def update_sprites(self):
        """ Search character by id """
        for z in reversed(range(0, len(self.layers))):
            for y in range(0, len(self.layers[z])):
                if not any(self.layers[z][y]):
                    continue
                for x in range(0, len(self.layers[z][y])):
                    element = self.layers[z][y][x]
                    if not element:
                        continue

                    if element.purge:
                        self.layers[z][y][x] = None
                    if element.replace_with:
                        self.layers[z][y][x] = element.replace_with

    def is_walkable(self, x, y):
        """ Check if a sprite  is walkable"""
        for z in reversed(self.layers):
            if not z[y][x]:
                continue

            if not z[y][x].walkable:
                return False

        return True

    def is_levelexit(self, x, y):
        """ Check if a sprite  is walkable"""
        for z in reversed(self.layers):
            try:
                if isinstance(z[y][x], LevelExit):
                    return True
            except IndexError:
                return False

        return False

    def search_character(self, id):
        """ Search character by id """
        for z in reversed(range(0, len(self.layers))):
            for y in range(0, len(self.layers[z])):
                if not any(self.layers[z][y]):
                    continue
                for x in range(0, len(self.layers[z][y])):
                    element = self.layers[z][y][x]
                    if element and element.id == id:
                        return (z, y, x)

        return (0, 0, 0)

    def search_sprite(self, sprite):
        """ Search character by id """
        for z in reversed(range(0, len(self.layers))):
            for y in range(0, len(self.layers[z])):
                if not any(self.layers[z][y]):
                    continue
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

    def calculate_next_pos(self, pos, direction):
        x, y = pos

        if direction == DIRECTION_LEFT:
            x -= 1
        elif direction == DIRECTION_RIGHT:
            x += 1
        if direction == DIRECTION_UP:
            y -= 1
        elif direction == DIRECTION_DOWN:
            y += 1

        if x < 0:
            x = 0

        if y < 0:
            y = 0

        return (x, y)

    def get_sprite(self, pos):
        z, y, x = pos

        try:
            return self.layers[z][y][x]
        except IndexError:
            return None
