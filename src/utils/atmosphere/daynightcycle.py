import time
import pygame
UPDATE_DATETIME_INTERVAL = 0.01 # Update the datetime lightning any X seconds
DARKEST_DATETIME = 200
BRIGHTES_DATETIME = 0

MODIFIER_DARK = 1
MODIFIER_LIGHT = -1


from PygameShader.shader import zoom, shader_bloom_fast1

class DayNightCycle:

    def __init__(self):
        self.daytime = 190
        self.daytime_updated = time.time()
        self.modifier = MODIFIER_DARK
        self.surface = None
        self.enabled = False

    def start(self):
        self.reset()


    def reset(self):
        self.daytime = 0
        self.daytime_updated = time.time()
        self.surface = None
        self.enabled = True

        pass

    def init_surface(self, screen):
        w, h = screen.get_size()
        self.surface = pygame.surface.Surface(
            (w, h), pygame.SRCALPHA | pygame.RLEACCEL).convert_alpha()

            
        self.surface.fill((0, 0, 0))

    def draw(self, screen):
        if not self.enabled:
            return

        if not self.surface:
            self.init_surface(screen)
            self.surface.set_alpha(self.daytime)

        # Todo: Split drawing and updating
        if time.time() - self.daytime_updated >= UPDATE_DATETIME_INTERVAL:
            self.daytime_updated = time.time()
            self.daytime += self.modifier
            print(self.daytime)
            self.surface.set_alpha(self.daytime)

            if self.daytime <= BRIGHTES_DATETIME:
                self.modifier = MODIFIER_DARK
            elif self.daytime >= DARKEST_DATETIME:
                self.modifier = MODIFIER_LIGHT

        # If Alpha is 0 don't draw the layer for performance reasons
        if self.daytime <= 0:
            return 

        self.surface.set_alpha(self.daytime)

        screen.blit((self.surface), (0, 0))