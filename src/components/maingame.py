import json.decoder
import logging
import math
import os
import random
import time
from threading import Thread
import pygame

import components.tobecontinued
import constants.game
import constants.graphics
import state.state
import utils.quality
import utils.savegame
from components.fadeable_component import FadeableComponent
from components.gameover import GameOver
from components.pausable_component import PausableComponent
from constants import direction
from constants import gamepad
from constants import keyboard
from constants.headup import BOTTOM_UI_HEIGHT
from constants.quality import QUALITY_LOW
from sprites.character import Character
from sprites.inlinesprite import InlineSprite
from state.level import Level, LAYER_MAINCHAR, LAYER_ITEMS
from utils.audio import play_sound
from utils.camera import Camera
from utils.level_editor import get_editor_blocks
from PygameShader.shader import bilinear

BACKDROP_COLOR = (36, 63, 64)

THREAD_INTERVAL_HIGH = 50
THREAD_INTERVAL_LOW = 500

class MainGame(PausableComponent, FadeableComponent):

    def __init__(self, data_dir, handle_change_component, settings_state, enable_edit_mode=False, gamepad=None):
        """ Constructor """
        super().__init__(data_dir, handle_change_component, settings_state, enable_edit_mode, gamepad)

        self.state = state.state.State(self.data_dir, self.gamepad)
        self.sprites_dir = os.path.join(self.data_dir, 'images', 'sprites')
        self.level = Level(self.sprites_dir, self.image_cache)
        self.camera = Camera()
        self.moving = None
        self.pressed_keys = []
        self.running = False
        self.editor_blocks_length = len(get_editor_blocks(self.sprites_dir, self.image_cache))
        self.editor_block_index = 0
        self.disable_ai = False
        self.async_ai_running = None
        self.is_level_exit = False
        self.last_rendered = None

        self.monotype_font = pygame.font.Font(
            os.path.join(data_dir, 'fonts', constants.game.MONOTYPE_FONT),
            constants.game.DEBUG_OUTPUT_FONT_SIZE)

        background_file = os.path.join(
            self.sprites_dir, 'backdrops', 'landscape.jpg'
        )

        self.backdrop = pygame.image.load(background_file).convert()

        # bilinear is faster than smoothscale for scaling down
        if self.settings_state.screen_resolution < self.backdrop.get_size():
            self.backdrop = bilinear(self.backdrop, self.settings_state.screen_resolution)
        else:
            self.backdrop = utils.quality.scale_method()(
            self.backdrop,
            self.settings_state.screen_resolution
            )

    def new_game(self):
        level_file = os.path.join(self.data_dir, 'levels', 'world.json')
        self.load_level(level_file)

    def load_savegame(self):
        """ Load savegame """
        level_file = utils.savegame.load_game(utils.savegame.DEFAULT_SAVE, self.state)
        self.load_level(level_file)

    def load_level(self, level_file, show_loading_screen=True):
        """ Load level from JSON file """
        self.level.level_file = level_file

        try:
            if show_loading_screen:
                self.level.load(self.loading_screen)
            else:
                self.level.load()
        except json.decoder.JSONDecodeError:
            logging.error('Invalid level JSON')
            return False

        z, y, x = self.level.search_character(constants.game.MAIN_CHARACTER_ID)
        self.level.layers[z][y][x].state = self.state.player_state

        self.update_camera()

        return True

    def loading_screen(self, percentage = None):
        """ Show loading screen """
        self.screen.fill(constants.headup.BOTTOM_UI_BACKGROUND)

        loading_text = _('Loading...')

        # Show percentage if given
        if(percentage is not None):
            percentage = str(percentage) + "%"
            percentage = percentage.rjust(4, ' ')

            loading_text += ' ' + str(percentage)


        # Render loading text
        rendered_text = self.monotype_font.render(
            loading_text,
            utils.quality.font_antialiasing(),
            (255, 255, 255)
        )

        # Calculate screen center
        pos_x, pos_y = self.screen.get_size()
        pos_x = pos_x / 2
        pos_y = pos_x / 2
        pos_x -= rendered_text.get_width() / 2
        pos_y -= rendered_text.get_height() / 2
        # draw text on screen
        self.screen.blit(rendered_text, (pos_x, pos_y))

        # Pump event queue and flip display to keep the application alive
        pygame.event.pump()
        pygame.display.flip()

    def mount(self):
        """ On mount hide mouse pointer and start music """
        pygame.mouse.set_visible(0)

        # CREDITS: https://audionautix.com/creative-commons-music
        atmo = 'level' + str(self.state.level) + '.ogg'
        self.play_music(atmo)

        self.fadein()

    def unmount(self):
        """ On unmount show mouse cursor and stop music """

        self.async_ai_running = False
        super().unmount()
        pygame.mouse.set_visible(1)
        pygame.mixer.music.stop()

    def update_screen(self, screen):
        if not self.level.loaded:
            return

        """ Update screen """
        if self.do_fade:
            screen = screen.copy().convert_alpha()

        sprite_width, sprite_height = constants.graphics.SPRITE_SIZE

        w, h = screen.get_size()

        h -= BOTTOM_UI_HEIGHT

        tolerance_x = math.ceil(w / sprite_width)
        tolerance_y = math.ceil(h / sprite_height)

        filtered_layers = list(self.level.layers)

        from_x = 0
        from_y = 0

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

        z = 0

        # TODO refactor to camera class
        virtscreen_h = len(filtered_layers[0]) * sprite_height
        virtscreen_w = len(filtered_layers[0][0]) * sprite_width

        if virtscreen_w > screen.get_width():
            virtscreen_w = screen.get_width()
        if virtscreen_h > screen.get_height():
            virtscreen_h = screen.get_height()
            virtscreen_h -= BOTTOM_UI_HEIGHT

        virtual_screen = pygame.surface.Surface((virtscreen_w, virtscreen_h))

        show_backdrop = False

        if self.settings_state.quality < QUALITY_LOW:
            show_backdrop = False
        elif virtscreen_h < screen.get_height() - BOTTOM_UI_HEIGHT:
            show_backdrop = True
        elif virtscreen_w < screen.get_width():
            show_backdrop = True

        if show_backdrop:
            screen.blit(self.backdrop, (0, 0, virtscreen_w, virtscreen_h))
        else:
            screen.fill(BACKDROP_COLOR)

        for layer in filtered_layers:
            y = 0
            x = 0

            draw_layer = True

            if self.state.show_only_layer is not None and z != self.state.show_only_layer:
                draw_layer = False

            for row in layer:
                for col in row:
                    if col and draw_layer:

                        pos_x, pos_y = col.calculate_pos(x, y)

                        if pos_x > virtscreen_w:
                            break
                        if pos_y > virtscreen_h:
                            break

                        col.draw(virtual_screen, x, y)

                        if self.state.edit_mode and isinstance(col, Character):
                            col.draw_debug(
                                virtual_screen,
                                x,
                                y,
                                from_x,
                                from_y
                            )

                    if isinstance(col, Character) and not self.disable_ai:
                        col.ai(self.level)

                    x += 1

                y += 1
                x = 0
            z += 1

        screen.blit(virtual_screen, (0, 0))

        # Draw head up display
        self.state.player_state.draw(screen)

        if self.do_fade:
            screen.set_alpha(self.alpha)
            self.screen.blit(screen, (0, 0))

        self.fade()

    def ai(self):
        if not self.async_ai_running:
            thread_fns = [
                self.async_low_prio,
                self.async_high_prio
            ]

            for fn in thread_fns:
                Thread(target=fn).start()

        for key in reversed(self.pressed_keys):
            if key in constants.keyboard.MOVEMENT_KEYS:
                self.moving = direction.key_to_direction(key)
                break

        if self.moving:
            self.move_main_character(self.moving)

        if self.is_level_exit:
            self.handle_change_component(components.tobecontinued.ToBeContinued)
            return

        if self.state.player_state.dead():
            self.moving = None
            self.update_screen(self.screen)
            super().unmount()
            component = self.handle_change_component(GameOver)
            component.state = self.state
            component.show_fps = self.show_fps
            return

    def async_low_prio(self):
        self.async_ai_running = True
        while self.async_ai_running and not self.do_quit:
            pygame.time.delay(THREAD_INTERVAL_LOW)
            self.check_for_updates()


    def check_for_updates(self):
        z, y, x = self.level.search_character(constants.game.MAIN_CHARACTER_ID)

        # Check if standing on level exit
        if not self.state.edit_mode and self.level.is_levelexit(x, y):
            # Show "To be continued"
            self.is_level_exit = True
            return

        # Check for level file changes
        if self.state.edit_mode and self.level.check_for_changes():
            # If the level file was changes do a reload
            self.load_level(self.level.level_file, False)

    def async_high_prio(self):
        self.async_ai_running = True
        while self.async_ai_running and not self.do_quit:
            pygame.time.delay(THREAD_INTERVAL_HIGH)
            self.handle_interactions()
            self.level.update_sprites()


    def handle_interactions(self):
        if self.state.player_state.use_item:
            z, y, x = self.level.search_character(constants.game.MAIN_CHARACTER_ID)
            character = self.level.get_sprite((z, y, x))

            for z in reversed(range(0, len(self.level.layers))):
                if isinstance(self.state.player_state.inventory, InlineSprite):
                    i_x, i_y = self.level.calculate_next_pos((x, y), character.direction)
                    i_element = self.level.get_sprite((z, i_y, i_x))
                    if i_element:
                        i_element.handle_interact_item(character)

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

    def grunt(self):
        """ Pig grunts """
        dirname = os.path.join(
            self.data_dir,
            'sounds',
            'pig'
        )

        files = [
            'grunt1.ogg',
            'grunt2.ogg',
            'grunt3.ogg',
            'grunt4.ogg',
            'grunt5.ogg',
        ]

        file = os.path.join(dirname, random.choice(files))

        play_sound(file)

        self.state.player_state.say(_('Grunz!'))

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
        self.pressed_keys.append(event.key)
        if event.key in keyboard.DISCARD_KEYS and self.state.player_state.show_detailed:
            self.state.player_state.show_detailed = None
        elif event.key == keyboard.K_CHANGE_BLOCK_DOWN:
            self.editor_block_index += 1
            length = len(get_editor_blocks(self.sprites_dir, self.image_cache))
            if self.editor_block_index >= length:
                self.editor_block_index = 0
        elif event.key == keyboard.K_CHANGE_BLOCK_UP:
            self.editor_block_index -= 1
            length = len(get_editor_blocks(self.sprites_dir, self.image_cache))
            if self.editor_block_index < 0:
                self.editor_block_index = length - 1
        elif event.key == keyboard.K_TOGGLE_EDIT_MODE and self.enable_edit_mode:
            self.toggle_edit_mode()
        elif event.key in keyboard.MOVEMENT_KEYS:
            self.move_main_character(direction.key_to_direction(event.key))
        elif event.key == keyboard.K_DROP_ITEM:
            self.drop_item()
        elif event.key == keyboard.K_GRUNT:
            self.grunt()
        elif event.key in keyboard.RUN_KEYS:
            self.running = True
        elif event.key == keyboard.K_USE:
            self.state.player_state.toggle_item()
        elif self.state.edit_mode:
            self.handle_edit_mode_event(event)

    def handle_keyup_event(self, event):
        """" Handle keyup events """

        if event.key in self.pressed_keys:
            self.pressed_keys.remove(event.key)

        if event.key in keyboard.MOVEMENT_KEYS:
            self.moving = None
        elif event.key in keyboard.RUN_KEYS:
            self.running = False

    def handle_joyhatmotion(self, event):
        """ Handle controller hat motion """
        x, y = event.value

        if x == 1:
            self.move_main_character(direction.DIRECTION_RIGHT)
            self.pressed_keys += constants.keyboard.K_RIGHT
        if x == -1:
            self.move_main_character(direction.DIRECTION_LEFT)
            self.pressed_keys += constants.keyboard.K_LEFT
        if y == 1:
            self.move_main_character(direction.DIRECTION_UP)
            self.pressed_keys += constants.keyboard.K_UP
        if y == -1:
            self.move_main_character(direction.DIRECTION_DOWN)
            self.pressed_keys += constants.keyboard.K_DOWN
        elif x == 0 and y == 0:
            self.moving = None
            self.pressed_keys = []


    def handle_joyaxismotion(self, event):
        """ Handle controller axis motion """
        value = round(event.value, 2)
        axis = event.axis

        # R2 modifier for running
        if axis == 5:
            self.running = value > 0
            return

        if axis == 0 and value > 0:
            self.move_main_character(direction.DIRECTION_RIGHT)
            self.pressed_keys += constants.keyboard.K_RIGHT
        if axis == 0 and value < 0:
            self.move_main_character(direction.DIRECTION_LEFT)
            self.pressed_keys += constants.keyboard.K_LEFT
        elif axis == 1 and value < 0:
            self.move_main_character(direction.DIRECTION_UP)
            self.pressed_keys += constants.keyboard.K_UP
        elif axis == 1 and value > 0:
            self.move_main_character(direction.DIRECTION_DOWN)
            self.pressed_keys += constants.keyboard.K_DOWN
        elif value == 0.0 or value > 3 or value < -3:
            self.moving = None
            self.pressed_keys = []

    def handle_joybuttondown(self, event):
        """ Handle joybutton press """
        if event.button == gamepad.K_CONFIRM:
            if self.state.player_state.show_detailed:
                self.state.player_state.show_detailed = None
            else:
                self.state.player_state.toggle_item()
        elif event.button == gamepad.K_DROP_ITEM:
            self.drop_item()
        elif event.button == gamepad.K_GRUNT:
            self.grunt()
        elif event.button == gamepad.K_RUN:
            self.running = True

    def handle_joybuttonup(self, event):
        """ Handle joy button up """
        if event.button == gamepad.K_RUN:
            self.running = False

    def handle_edit_mode_event(self, event):
        """ Handle edit mode events """
        if self.state.edit_mode and event.key == keyboard.K_SAVE_LEVEL:
            self.level.save()
            self.state.player_state.say(_('Level saved.'))
        elif self.state.edit_mode and event.key == keyboard.K_DUMP_LEVEL:
            self.level.dump()
            self.state.player_state.say(_('Level dumped.'))
        elif self.state.edit_mode and event.key in keyboard.NUMERIC_KEYS:
            index = keyboard.NUMERIC_KEYS.index(event.key)
            # Shift is the key for running
            # Shift + Number sets null
            self.make_field(index, self.running)

        elif self.state.edit_mode and event.key == keyboard.K_NEXT_LAYER:
            self.next_layer()

    def make_field(self, z, clear=False):
        """ Make field in edit mode """
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

    def next_layer(self):
        """ Toggle layers in edit mode"""
        if self.state.show_only_layer is None:
            self.state.show_only_layer = -1

        self.state.show_only_layer += 1

        if self.state.show_only_layer >= len(self.level.layers):
            self.state.show_only_layer = None

    def toggle_edit_mode(self):
        """ Toggle edit mode """
        self.state.edit_mode = not self.state.edit_mode
        self.state.show_only_layer = None

    def move_main_character(self, dir):
        """ Move main character one field in direction """
        z, y, x = self.level.search_character(constants.game.MAIN_CHARACTER_ID)
        character = self.level.layers[z][y][x]

        if not self.moving:
            self.moving = dir
            character.last_movement = 0
            return

        walk_speed = character.walk_speed

        if self.running:
            walk_speed = character.sprint_speed

        if time.time() - character.last_movement < walk_speed:
            return

        character.last_movement = time.time()

        next_x = x
        next_y = y

        if dir == direction.DIRECTION_UP:
            next_y -= 1
        elif dir == direction.DIRECTION_LEFT:
            next_x -= 1
        elif dir == direction.DIRECTION_RIGHT:
            next_x += 1
        elif dir == direction.DIRECTION_DOWN:
            next_y += 1

        character.change_direction(dir)

        if (next_y < 0):
            return

        if (next_x < 0):
            return

        if (next_y > len(self.level.layers[z]) - 1):
            return

        if (next_x > len(self.level.layers[z][y]) - 1):
            return

        layer_count = len(self.level.layers)

        walkable = self.level.is_walkable(next_x, next_y)

        for layer in range(0, layer_count):
            element = self.level.get_sprite((layer, next_y, next_x))

            if element:
                element.handle_interact(character)

        if self.state.edit_mode:
            walkable = True

        if walkable:
            self.level.layers[z][next_y][next_x] = character
            self.level.layers[z][y][x] = None

            self.update_camera()
