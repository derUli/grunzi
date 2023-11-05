import json.decoder
import logging
import math
import os
import time

import constants.game
import constants.graphics
import state.state
import utils.savegame
from components.component import Component
from components.gameover import GameOver
from components.pausable_component import PausableComponent
from components.tobecontinued import ToBeContinued
from constants import gamepad
from constants.direction import *
from constants.headup import BOTTOM_UI_HEIGHT
from constants.keyboard import *
from sprites.character import Character
from state.level import Level, LAYER_MAINCHAR, LAYER_ITEMS
from utils.audio import play_sound
from utils.camera import Camera
from utils.level_editor import get_editor_blocks
from components.fadeable_component import FadeableComponent

class MainGame(PausableComponent, FadeableComponent):

    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad)

        self.state = state.state.State(self.data_dir, self.gamepad)
        self.sprites_dir = os.path.join(self.data_dir, 'images', 'sprites')
        self.level = Level(self.sprites_dir, self.image_cache)
        self.camera = Camera()
        self.moving = None
        self.running = False
        self.editor_blocks_length = len(get_editor_blocks(self.sprites_dir, self.image_cache))
        self.editor_block_index = 0
        background_file = os.path.join(
            self.sprites_dir, 'backdrops', 'landscape.jpg'
        )

        self.backdrop = pygame.image.load(background_file).convert_alpha()
        self.backdrop = pygame.transform.smoothscale(
            self.backdrop,
            self.settings_state.screen_resolution
        )

    def load_savegame(self):
        """ Load savegame """
        level_file = utils.savegame.load_game(utils.savegame.DEFAULT_SAVE, self.state)
        self.load_level(level_file)

    def load_level(self, level_file):
        """ Load level from JSON file """
        self.level.level_file = level_file

        try:
            self.level.load()
        except json.decoder.JSONDecodeError:
            logging.error('Invalid level JSON')
            return False

        z, y, x = self.level.search_character(constants.game.MAIN_CHARACTER_ID)
        self.level.layers[z][y][x].state = self.state.player_state

        self.update_camera()

        return True

    def mount(self):
        """ On mount hide mouse pointer and start music """
        pygame.mouse.set_visible(0)

        # CREDITS: https://audionautix.com/creative-commons-music
        atmo = 'level' + str(self.state.level) + '.ogg'
        self.play_music(atmo)

        level_file = os.path.join(self.data_dir, 'levels', 'level1.json')
        self.load_level(level_file)

        self.fadein()

    def unmount(self):
        """ On unmount show mouse cursor and stop music """
        pygame.mouse.set_visible(1)
        pygame.mixer.music.stop()

        self.fadeout()

    def update_screen(self, screen):
        screen = screen.copy().convert_alpha()

        """ Draw screen """
        if self.moving:
            self.move_main_character(self.moving)

        self.level.purge_sprites()
        sprite_width, sprite_height = constants.graphics.SPRITE_SIZE

        w, h = screen.get_size()

        h -= BOTTOM_UI_HEIGHT
        virtual_screen = pygame.surface.Surface((w, h))

        virtual_screen.blit(self.backdrop, (0, 0))

        tolerance_x = math.ceil(w / sprite_width)
        tolerance_y = math.ceil(h / sprite_height)

        filtered_layers = list(self.level.layers)

        for z in range(0, len(filtered_layers)):
            from_y = self.camera.y - math.ceil(tolerance_y / 2)
            to_y = self.camera.y + tolerance_y

            from_x = self.camera.x - math.ceil(tolerance_x / 2)
            to_x = self.camera.x + tolerance_x

            if from_y < 0:
                from_y = 0

            if from_x < 0:
                from_x = 0

            filtered_layers[z] = filtered_layers[z][from_y:to_y]

            for y in range(0, len(filtered_layers[z])):
                filtered_layers[z][y] = filtered_layers[z][y][from_x:to_x]

        for layer in filtered_layers:
            y = 0
            x = 0
            for row in layer:
                for col in row:
                    if col:
                        col.draw(virtual_screen, x, y)

                    if isinstance(col, Character):
                        new_pos = col.ai(self.level)

                    x += 1

                y += 1
                x = 0

        screen.blit(virtual_screen, (0, 0))

        self.draw_headup(screen)

        if self.state.player_state.dead():
            component = self.handle_change_component(GameOver)
            component.state = self.state

        # Check for changes
        if self.state.edit_mode and self.level.check_for_changes():
            # If the level file was changes do a reload
            self.load_level(self.level.level_file)

        screen.set_alpha(self.alpha)

        self.screen.blit(screen, (0,0))

        self.fade()

    def drop_item(self):
        z, y, x = self.level.search_character(constants.game.MAIN_CHARACTER_ID)

        beep_sound = os.path.join(
            self.data_dir,
            'sounds',
            'common',
            'beep.ogg'
        )

        if not self.state.player_state.inventory:
            play_sound(beep_sound)
            logging.debug("Drop item failed. No item in inventory.")
            return

        if self.level.layers[LAYER_ITEMS][y][x]:
            play_sound(beep_sound)
            logging.debug("Drop item failed. Static objects layer not empty")
            return

        self.state.player_state.inventory.purge = False
        self.level.layers[LAYER_ITEMS][y][x] = self.state.player_state.inventory

        self.state.player_state.inventory = None

    def update_camera(self):
        z, y, x = self.level.search_character(constants.game.MAIN_CHARACTER_ID)

        if x < 0:
            x = 0

        if y < 0:
            y = 0

        self.camera.x = x
        self.camera.y = y

    def handle_event(self, event):
        """ Handle events """
        super().handle_event(event)

        if event.type == pygame.KEYUP:
            self.handle_keyup_event(event)
        elif event.type == pygame.KEYDOWN:
            self.handle_keydown_event(event)
        elif event.type == pygame.JOYBUTTONDOWN:
            self.handle_joybuttondown(event)
        elif event.type == pygame.JOYBUTTONUP:
            self.handle_joybuttonup(event)
        elif event.type == pygame.JOYHATMOTION:
            self.handle_joyhatmotion(event)
        elif event.type == pygame.JOYAXISMOTION:
            self.handle_joyaxismotion(event)

    def handle_keydown_event(self, event):
        """" Handle keydown events """
        if event.key in DISCARD_KEYS and self.state.player_state.show_detailed:
            self.state.player_state.show_detailed = None
        elif event.key == K_CHANGE_BLOCK_DOWN:
            self.editor_block_index += 1
            length = len(get_editor_blocks(self.sprites_dir, self.image_cache))
            if self.editor_block_index >= length:
                self.editor_block_index = 0
        elif event.key == K_CHANGE_BLOCK_UP:
            self.editor_block_index -= 1
            length = len(get_editor_blocks(self.sprites_dir, self.image_cache))
            if self.editor_block_index < 0:
                self.editor_block_index = length - 1
        elif event.key == K_TOGGLE_EDIT_MODE and self.enable_edit_mode:
            self.state.edit_mode = not self.state.edit_mode
        elif self.state.edit_mode and event.key == K_SAVE_LEVEL:
            self.level.save()
        elif self.state.edit_mode and event.key in NUMERIC_KEYS:
            index = NUMERIC_KEYS.index(event.key)
            # Shift is the key for running
            # Shift + Number sets null
            self.make_field(index, self.running)
        elif event.key == K_LEFT:
            self.move_main_character(DIRECTION_LEFT)
        elif event.key == K_RIGHT:
            self.move_main_character(DIRECTION_RIGHT)
        elif event.key == K_UP:
            self.move_main_character(DIRECTION_UP)
        elif event.key == K_DOWN:
            self.move_main_character(DIRECTION_DOWN)
        elif event.key == K_DROP_ITEM:
            self.drop_item()
        elif event.key == K_RUN:
            self.running = True

    def handle_keyup_event(self, event):
        """" Handle keyup events """
        if event.key in MOVEMENT_KEYS:
            self.moving = None
        elif event.key == K_RUN:
            self.running = False

    def handle_joyhatmotion(self, event):
        """ Handle controller hat motion """
        x, y = event.value

        if x == 1:
            self.move_main_character(DIRECTION_RIGHT)
        elif x == -1:
            self.move_main_character(DIRECTION_LEFT)
        elif y == 1:
            self.move_main_character(DIRECTION_UP)
        elif y == -1:
            self.move_main_character(DIRECTION_DOWN)
        elif x == 0 and y == 0:
            self.moving = None

    def handle_joyaxismotion(self, event):
        """ Handle controller axis motion """
        value = round(event.value, 2)
        axis = event.axis

        # R2 modifier for running
        if axis == 5:
            self.running = value > 0
            return

        if value == 0.0 or value > 3 or value < -3:
            self.moving = None

        if axis == 0 and value > 0:
            self.move_main_character(DIRECTION_RIGHT)
        if axis == 0 and value < 0:
            self.move_main_character(DIRECTION_LEFT)
        elif axis == 1 and value < 0:
            self.move_main_character(DIRECTION_UP)
        elif axis == 1 and value > 0:
            self.move_main_character(DIRECTION_DOWN)

    def handle_joybuttondown(self, event):
        """ Handle joybutton press """
        if event.button == gamepad.K_CONFIRM:
            self.state.player_state.show_detailed = None
        elif event.button == gamepad.K_DROP_ITEM:
            self.drop_item()
        elif event.button == gamepad.K_RUN:
            self.running = True

    def handle_joybuttonup(self, event):
        """ Handle joy button up """
        if event.button == gamepad.K_RUN:
            self.running = False

    def make_field(self, z, clear=False):
        _z, y, x = self.level.search_character(constants.game.MAIN_CHARACTER_ID)

        if z >= len(self.level.layers):
            return

        if z == LAYER_MAINCHAR:
            return

        if clear:
            self.level.layers[z][y][x] = None
            return

        editor_blocks = get_editor_blocks(self.sprites_dir, self.image_cache)
        editor_block = editor_blocks[self.editor_block_index]

        self.level.layers[z][y][x] = editor_block

    def move_main_character(self, direction):
        z, y, x = self.level.search_character(constants.game.MAIN_CHARACTER_ID)
        character = self.level.layers[z][y][x]

        if not self.moving:
            self.moving = direction
            character.last_move = 0
            return

        walk_speed = character.walk_speed

        if self.running:
            walk_speed = character.sprint_speed

        if time.time() - character.last_move < walk_speed:
            return

        character.last_move = time.time()

        next_x = x
        next_y = y

        if direction == DIRECTION_UP:
            next_y -= 1
        elif direction == DIRECTION_LEFT:
            next_x -= 1
        elif direction == DIRECTION_RIGHT:
            next_x += 1
        elif direction == DIRECTION_DOWN:
            next_y += 1

        character.change_direction(direction)

        if (next_y < 0):
            return

        if (next_x < 0):
            return

        if (next_y > len(self.level.layers[z]) - 1):
            return

        if (next_x > len(self.level.layers[z][y]) - 1):
            return

        layer_count = len(self.level.layers)

        for layer in range(0, layer_count):
            element = self.level.layers[layer][next_y][next_x]
            if element:
                element.handle_interact(character)

        walkable = self.level.is_walkable(next_x, next_y)

        if self.state.edit_mode:
            walkable = True

        if walkable:
            self.level.layers[z][next_y][next_x] = character
            self.level.layers[z][y][x] = None

            self.update_camera()

        if self.level.is_levelexit(next_x, next_y) and not self.state.edit_mode:
            # TODO: Show "To be continued"
            self.handle_change_component(ToBeContinued)

    def draw_headup(self, screen):
        """ Draw head up display """
        self.state.player_state.draw(screen)
