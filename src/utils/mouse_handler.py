import os
import pygame
from constants.headup import BOTTOM_UI_HEIGHT
from constants.graphics import SPRITE_SIZE
from constants.direction import DIRECTION_RIGHT, DIRECTION_UP, DIRECTION_LEFT, DIRECTION_DOWN
COLOR_POINTER_DEFAULT = (255,255,255)

POINTER_UP = 'up'
POINTER_RIGHT = 'right'
POINTER_DOWN = 'down'
POINTER_LEFT = 'left'
COLOR_POINTER_ACTION = (0, 0, 0)
DOUBLECLICK_SPEED = 500

class MouseHandler:

    def __init__(self, data_dir, handle_move, handle_toggle_item, handle_grunt, handle_drop_item):
        self.enabled = False
        self.pointer = None
        self.data_dir  = data_dir

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

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def pointer_rect(self):
        x, y = pygame.mouse.get_pos()
        w, h = SPRITE_SIZE

        return pygame.rect.Rect((x, y, w, h))

    def handle_mouseup(self):
        if not self.enabled:
            return

        self.mousedown = False
        self.running = False
        self.handle_move(None)

    def init_pointers(self):
        cursor_dir = os.path.join( self.data_dir, 'images', 'pointers')
        return {

                POINTER_UP:  pygame.image.load(os.path.join(cursor_dir, 'arrow_up.png')).
                convert_alpha(),
                POINTER_RIGHT: pygame.image.load(os.path.join(cursor_dir, 'arrow_right.png')).
                convert_alpha(),
                POINTER_DOWN: pygame.image.load(os.path.join(cursor_dir, 'arrow_down.png')).
                convert_alpha(),
                POINTER_LEFT: pygame.image.load(os.path.join(cursor_dir, 'arrow_left.png')).
                convert_alpha()

        }

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

        color = COLOR_POINTER_DEFAULT
        pointer = None

        if self.mousedown:
            self.handle_mousedown()

        for hotspot in self.movement_hotspots():
            if rect.colliderect(hotspot['rect']):
                pointer = hotspot['pointer']
                break

        if rect.colliderect(headup_display):
            color = COLOR_POINTER_DEFAULT

        if not self.inventory_display:
            self.inventory_display = inventory_display
            self.inventory_display.y += self.screen.get_height() - BOTTOM_UI_HEIGHT

        if not self.health_display:
            self.health_display = health_display
            self.health_display.y += self.screen.get_height() - BOTTOM_UI_HEIGHT

        # Inventory click
        if rect.colliderect(self.inventory_display):
            color = COLOR_POINTER_ACTION

        # Health click
        if rect.colliderect(self.health_display):
            color = COLOR_POINTER_ACTION

        if rect.colliderect(mainchar_rect):
            color = COLOR_POINTER_ACTION

        if pointer:
            screen.blit(pointer, (rect.x, rect.y))
            return

        pygame.draw.rect(screen, color, rect)