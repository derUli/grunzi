import pygame
from constants.headup import BOTTOM_UI_HEIGHT
from constants.direction import DIRECTION_RIGHT, DIRECTION_UP, DIRECTION_LEFT, DIRECTION_DOWN
COLOR_POINTER_DEFAULT = (255,255,255)
COLOR_POINTER_MOVE_UP = (255,0,0)
COLOR_POINTER_MOVE_DOWN = (255,255,0)
COLOR_POINTER_MOVE_LEFT = (255,0,255)
COLOR_POINTER_MOVE_RIGHT = (0,255,255)
COLOR_POINTER_ACTION = (0, 0, 0)
DOUBLECLICK_SPEED = 500

POINTER_SIZE = 16

class MouseHandler:

    def __init__(self, handle_move, handle_toggle_item, handle_grunt, handle_drop_item):
        self.enabled = False
        self.pointer = None
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

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def pointer_rect(self):
        x, y = pygame.mouse.get_pos()
        w, h = POINTER_SIZE, POINTER_SIZE

        return pygame.rect.Rect((x, y, w, h))

    def handle_mouseup(self):
        if not self.enabled:
            return

        self.mousedown = False
        self.running = False
        self.handle_move(None)

    def handle_mousedown(self):
        if not self.enabled:
            return

        if not self.mainchar_rect:
            return

        rect = self.pointer_rect()

        if rect.colliderect(self.inventory_display):
            self.handle_toggle_item()
            return

        if rect.colliderect(self.health_display):
            self.handle_grunt()
            return


        if rect.colliderect(self.mainchar_rect):
            self.handle_drop_item()
            return

        if not self.mousedown and self.dbclock.tick() < DOUBLECLICK_SPEED:
            self.running = True

        self.mousedown = True
        direction = None

        for hotspot in self.movement_hotspots():
            if hotspot['rect'].colliderect(rect):
                direction = hotspot['direction']

        self.handle_move(direction, self.running)

    def movement_hotspots(self):
        screen = self.screen
        mainchar_rect = self.mainchar_rect

        hotspots = []

        hotspots.append(
            {
                'rect': pygame.rect.Rect(
                    mainchar_rect.x + mainchar_rect.w,
                    0,
                    screen.get_width(),
                    mainchar_rect.y + mainchar_rect.h,
                ),
                'direction': DIRECTION_RIGHT,
                'color': COLOR_POINTER_MOVE_RIGHT
            })

        hotspots.append(
            {
                'rect': pygame.rect.Rect(
                    0,
                    0,
                    mainchar_rect.x,
                    mainchar_rect.y + mainchar_rect.h,
                ),
                'direction': DIRECTION_LEFT,
                'color': COLOR_POINTER_MOVE_LEFT
            })

        hotspots.append(
            {
                'rect': pygame.rect.Rect(
                    0,
                    0,
                    screen.get_width(),
                    mainchar_rect.y
                ),
                'direction': DIRECTION_UP,
                'color': COLOR_POINTER_MOVE_UP
            })

        hotspots.append(
            {
                'rect': pygame.rect.Rect(
                    0,
                    mainchar_rect.y + mainchar_rect.h,
                    screen.get_width(),
                    screen.get_height() - mainchar_rect.y + mainchar_rect.h
                ),
                'direction': DIRECTION_DOWN,
                'color': COLOR_POINTER_MOVE_DOWN
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

        if self.mousedown:
            self.handle_mousedown()

        for hotspot in self.movement_hotspots():
            if rect.colliderect(hotspot['rect']):
                color = hotspot['color']


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

        pygame.draw.rect(screen, color, rect)