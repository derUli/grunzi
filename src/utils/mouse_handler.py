import os

import pygame

from constants.direction import DIRECTION_RIGHT, DIRECTION_UP, DIRECTION_LEFT, DIRECTION_DOWN
from constants.graphics import SPRITE_SIZE
from constants.headup import BOTTOM_UI_HEIGHT
from utils.quality import scale_method

POINTER_UP = 'up'
POINTER_RIGHT = 'right'
POINTER_DOWN = 'down'
POINTER_LEFT = 'left'
POINTER_ACTION = 'action'
POINTER_DEFAULT = 'default'

POINTER_SIZE = (32, 32)
DOUBLECLICK_SPEED = 500


class MouseHandler:

    def __init__(self, data_dir, handle_move, handle_toggle_item, handle_grunt, handle_drop_item):
        self.enabled = False
        self.pointer = None
        self.data_dir = data_dir

        self.handle_move = handle_move
        self.handle_toggle_item = handle_toggle_item
        self.handle_grunt = handle_grunt
        self.health_display = None
        self.handle_drop_item = handle_drop_item
        self.mainchar_rect = None
        self.screen = None
        self.mousedown = False
        self.running = False
        self.dbclock = pygame.time.Clock()
        self.inventory_display = None
        self.pointers = self.init_pointers()
        self.pointer = None

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def pointer_rect(self):
        x, y = pygame.mouse.get_pos()
        w, h = SPRITE_SIZE

        if self.pointer:
            w, h = self.pointer.get_size()

        return pygame.rect.Rect((x, y, w, h))

    def handle_mouseup(self):
        if not self.enabled:
            return

        self.mousedown = False
        self.running = False
        self.handle_move(None)

    def init_pointers(self):
        cursor_dir = os.path.join(self.data_dir, 'images', 'pointers')
        pointers = {

            POINTER_UP: pygame.image.load(os.path.join(cursor_dir, 'arrow_up.png')).convert_alpha(),
            POINTER_RIGHT: pygame.image.load(os.path.join(cursor_dir, 'arrow_right.png')).convert_alpha(),
            POINTER_DOWN: pygame.image.load(os.path.join(cursor_dir, 'arrow_down.png')).convert_alpha(),
            POINTER_LEFT: pygame.image.load(os.path.join(cursor_dir, 'arrow_left.png')).convert_alpha(),
            POINTER_ACTION: pygame.image.load(os.path.join(cursor_dir, 'action.png')).convert_alpha(),
            POINTER_DEFAULT: pygame.image.load(os.path.join(cursor_dir, 'default.png')).convert_alpha(),
        }

        scale = scale_method()
        for key in pointers:
            pointers[key] = scale(pointers[key], POINTER_SIZE)

        return pointers

    def handle_mousedown(self):
        if not self.enabled:
            return

        if not self.mainchar_rect:
            return

        rect = self.pointer_rect()

        if not self.mousedown and rect.colliderect(self.inventory_display):
            self.handle_toggle_item()
            return

        if not self.mousedown and rect.colliderect(self.health_display):
            self.handle_grunt()
            return

        if not self.mousedown and rect.colliderect(self.mainchar_rect):
            self.handle_drop_item()
            return

        if not self.mousedown and self.dbclock.tick() < DOUBLECLICK_SPEED:
            self.running = True

        self.mousedown = True
        direction = None

        for hotspot in self.movement_hotspots():
            if hotspot['rect'].colliderect(rect):
                direction = hotspot['direction']
                break

        self.handle_move(direction, self.running)

    def movement_hotspots(self):
        screen = self.screen
        mainchar_rect = self.mainchar_rect
        sw, sh = SPRITE_SIZE

        hotspots = []

        hotspots.append(
            {
                'rect': pygame.rect.Rect(
                    mainchar_rect.x + mainchar_rect.w,
                    mainchar_rect.y - (mainchar_rect.h * 2),
                    screen.get_width() - (mainchar_rect.x + mainchar_rect.w) - 5,
                    (sh * 4),
                ),
                'direction': DIRECTION_RIGHT,
                'pointer': self.pointers[POINTER_RIGHT]
            })

        hotspots.append(
            {
                'rect': pygame.rect.Rect(
                    0,
                    mainchar_rect.y - (mainchar_rect.h * 2),
                    mainchar_rect.x,
                    (sh * 4),
                ),
                'direction': DIRECTION_LEFT,
                'pointer': self.pointers[POINTER_LEFT]
            })

        hotspots.append(
            {
                'rect': pygame.rect.Rect(
                    0,
                    0,
                    screen.get_width(),
                    mainchar_rect.y - (mainchar_rect.h * 2)
                ),
                'direction': DIRECTION_UP,
                'pointer': self.pointers[POINTER_UP]
            })

        hotspots.append(
            {
                'rect': pygame.rect.Rect(
                    0,
                    mainchar_rect.y + (mainchar_rect.h * 2),
                    self.screen.get_width(),
                    (sh * 3),
                ),
                'direction': DIRECTION_DOWN,
                'pointer': self.pointers[POINTER_DOWN]
            })

        hotspots.append(
            {
                'rect': pygame.rect.Rect(
                    mainchar_rect.x,
                    mainchar_rect.y + mainchar_rect.h,
                    mainchar_rect.w,
                    mainchar_rect.h,
                ),
                'direction': DIRECTION_DOWN,
                'pointer': self.pointers[POINTER_DOWN]
            })

        hotspots.append(
            {
                'rect': pygame.rect.Rect(
                    mainchar_rect.x,
                    0,
                    mainchar_rect.w,
                    mainchar_rect.y,
                ),
                'direction': DIRECTION_UP,
                'pointer': self.pointers[POINTER_UP]
            })

        return hotspots

    def draw(
            self,
            screen,
            mainchar_rect,
            headup_display,
            inventory_display,
            health_display
    ):
        if not self.enabled:
            return

        rect = self.pointer_rect()

        self.screen = screen
        self.mainchar_rect = mainchar_rect

        if self.mousedown:
            self.handle_mousedown()

        pointer = self.pointers[POINTER_DEFAULT]

        for hotspot in self.movement_hotspots():
            if rect.colliderect(hotspot['rect']):
                pointer = hotspot['pointer']
                break

        if not self.inventory_display:
            self.inventory_display = inventory_display
            self.inventory_display.y += self.screen.get_height() - BOTTOM_UI_HEIGHT

        if not self.health_display:
            self.health_display = health_display
            self.health_display.y += self.screen.get_height() - BOTTOM_UI_HEIGHT

        # Inventory click
        if rect.colliderect(self.inventory_display):
            pointer = self.pointers[POINTER_ACTION]

        # Health click
        if rect.colliderect(self.health_display):
            pointer = self.pointers[POINTER_ACTION]

        if rect.colliderect(mainchar_rect):
            pointer = self.pointers[POINTER_ACTION]

        self.pointer = pointer

        if pointer:
            screen.blit(pointer, (rect.x, rect.y))
            return
