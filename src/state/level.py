""" Level """
import json
import logging
import os
import time

import pygame

import constants.graphics
import sprites.sprite
from constants.direction import DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_UP
from constants.game import MAIN_CHARACTER_ID
from sprites.levelexit import LevelExit
from utils.screenshot import make_screenshot, DUMP_DIR

LAYER_GROUND = 0
LAYER_STATIC_OBJECTS = 1
LAYER_ITEMS = 2
LAYER_OTHER_CHARS = 3
LAYER_MAINCHAR = 4


class Level:
    """ Level class """

    def __init__(self, sprites_dir, image_cache, level_file=None):
        """ Contructor """
        self.layers = []
        self.sprites_dir = sprites_dir
        self.image_cache = image_cache
        self.loaded = False
        self.level_file = level_file
        self.level_file_last_changed = None
        self.original_layers = []

    def load(self, progress_callback=None):
        """ Load level file """
        load_start = time.time()
        layers = []
        self.level_file_last_changed = os.path.getmtime(self.level_file)

        with open(self.level_file, 'r') as f:
            leveldata = json.loads(f.read())

        if progress_callback:
            progress_callback(0)

        one_percent = 100 / self.total_blocks(leveldata)
        loaded_percent = 0
        loaded_blocks = 0

        mainchar_added = False

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

                    if not x:
                        next

                    sprite = sprites.sprite.from_dict(
                        x, self.sprites_dir, self.image_cache)

                    if sprite and sprite.id == MAIN_CHARACTER_ID:
                        if mainchar_added:
                            sprite = None
                        mainchar_added = True
                    elif sprite:
                        sprite.preload()

                    row.append(sprite)

                layer.append(row)
            layers.append(layer)

        self.layers = layers
        self.original_layers = self.to_saveable_list()
        self.loaded = True

        load_end = time.time()
        load_time = load_end - load_start
        logging.debug("Map loaded in " + str(load_time) + ' seconds')

    def to_diff_list(self):
        """
            Save games contains only changes to the initial level state
            Generate list which will be saved JSON serialized
        """
        update_list = self.to_saveable_list()
        for z in range(len(update_list)):
            for y in range(len(update_list[z])):
                for x in range(len(update_list[z][y])):
                    old_value = self.original_layers[z][y][x]
                    new_value = update_list[z][y][x]

                    if isinstance(
                            new_value, dict) and 'attributes' in new_value and new_value['attributes']:
                        continue
                    if new_value == old_value:
                        update_list[z][y][x] = None
                    elif not bool(new_value) and bool(old_value):
                        update_list[z][y][x] = 'removed'

        return update_list

    def apply_diff(self, update_list):
        """ Apply diff from savegame to loaded level """
        for z in range(len(update_list)):
            for y in range(len(update_list[z])):
                if not any(update_list[z][y]):
                    continue
                for x in range(len(update_list[z][y])):
                    new_value = update_list[z][y][x]

                    if new_value == 'removed':
                        self.layers[z][y][x] = None
                    elif new_value is not None:
                        self.layers[z][y][x] = sprites.sprite.from_dict(
                            new_value, self.sprites_dir, self.image_cache)

    def save(self, progress_callback=None):
        """ Save level """
        if progress_callback:
            progress_callback(
                percentage=None,
                loading_text=_('Saving level...'))
        with open(self.level_file, 'w') as f:
            f.write(json.dumps(self.to_saveable_list(), indent=0))

    def dump(self, progress_callback=None):
        start_time = time.time()

        """ Dump map  to image """
        w, h = constants.graphics.SPRITE_SIZE

        total_w = len(self.layers[0][0]) * w
        total_h = len(self.layers[0]) * h

        one_percent = 100 / self.total_blocks(self.layers)
        loaded_percent = 0
        loaded_blocks = 0

        waiting_text = _('Dumping level to image...')
        progress_callback(loaded_percent, waiting_text)

        surface = pygame.surface.Surface((total_w, total_h))

        for z in range(0, len(self.layers)):
            for y in range(0, len(self.layers[z])):
                for x in range(0, len(self.layers[z][y])):
                    element = self.layers[z][y][x]

                    loaded_blocks += 1
                    percentage = round(one_percent * loaded_blocks)

                    if percentage != loaded_percent:
                        loaded_percent = percentage

                        if progress_callback:
                            progress_callback(loaded_percent, waiting_text)

                    if element:
                        if hasattr(element, 'animation'):
                            animation = element.animation
                            # Wait for animation frame loading
                            animation.reload()
                            # wait for animation loaded
                            while not animation.fully_loaded():
                                continue

                        element.draw(surface, x, y)

        make_screenshot(surface, DUMP_DIR)

        end_time = time.time()

        logging.debug(f'Map dumped in {str(end_time - start_time)} seconds')

    def total_blocks(self, leveldata):
        """ Calculate total blocks count for progress bar"""
        total_blocks = 0

        for z in leveldata:
            for y in z:
                for x in y:
                    total_blocks += 1

        return total_blocks

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
        """ Check if a position  is walkable"""
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

    def search_by_id(self, id):
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
                try:
                    x = self.layers[z][y].index(sprite)
                    return (z, y, x)
                except ValueError:
                    continue

        return (0, 0, 0)

    def move_sprite(self, sprite, target_pos):
        """ Move a sprite to target pos """
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
        """ Calculate next pos for movement """
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
        """ Get sprite at """
        z, y, x = pos

        try:
            return self.layers[z][y][x]
        except IndexError:
            return None

    def update_camera(self, camera):
        z, y, x = self.search_by_id(constants.game.MAIN_CHARACTER_ID)
        camera.update(x, y)

    def async_ai(self):
        for z in self.layers:
            for y in z:
                if not any(y):
                    continue

                for x in y:
                    if isinstance(x, sprites.sprite.AsyncAI):
                        x.async_ai(self)
