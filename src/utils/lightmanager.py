import arcade
from arcade.experimental.lights import LightLayer, Light

LIGHTING_DARK = 'dark'

class LightManager:
    def __init__(self):
        self.light_layer = None
        self.lights = {}
        self._type = None

    def reset(self):
        self._type = type
        self.lights = {}
        self.light_layer = None
    def setup(self, args):
        self.reset()

        self._type = args.state.difficulty.options['lighting']

        if self._type is None:
            return

        w, h = arcade.get_window().get_size()

        self.light_layer = LightLayer(w, h)

        if self._type == LIGHTING_DARK:
            self.setup_dark(args)


    def update(self, args):
        if not self.enabled:
            return

        self.lights['player_light'].position = args.player.position

    def draw(self):
        if not self.enabled:
            return

        self.light_layer.draw()

    def setup_dark(self, args):
        self.lights['player_light'] = Light(
            args.player.center_x,
            args.player.center_y,
            150,
            arcade.color.WHITE,
            'soft'
        )

        self.light_layer.add(self.lights['player_light'])

    @property
    def enabled(self):
        return self._type is not None
