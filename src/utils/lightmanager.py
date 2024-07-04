import arcade
from arcade.experimental.lights import LightLayer, Light

LIGHTING_DARK = 'dark'
LIGHT_LAYER_LANTERN = 'lantern'


class LightManager:
    def __init__(self):
        """ Constructor """

        self.light_layer = None
        self.lights = {}
        self._type = None

    def reset(self):
        """ Reset light manager """

        self._type = type
        self.lights = {}
        self.light_layer = None

    def setup(self, args) -> None:
        """ Setup light manager """

        self.reset()

        self._type = args.state.difficulty.options['lighting']

        if self._type is None:
            return

        w, h = arcade.get_window().get_size()
        self.light_layer = LightLayer(w, h)

        if self._type == LIGHTING_DARK:
            self.setup_dark(args)

    def setup_dark(self, args) -> None:
        """ Setup lighting for dark levels """

        self.lights[LIGHT_LAYER_LANTERN] = Light(
            args.player.center_x,
            args.player.center_y,
            150,
            arcade.color.WHITE,
            'soft'
        )

    def update(self, args):
        """ Update light"""

        if not self.enabled:
            return

        if self._type == LIGHTING_DARK:
            self.update_dark(args)

    def update_dark(self, args):
        """ Update dark lighting """

        from constants.layers import LAYER_LANTERN

        source = arcade.sprite.SpriteSolidColor(1, 1, arcade.csscolor.BLACK)

        if len(args.scene[LAYER_LANTERN]) > 0:
            source = args.scene[LAYER_LANTERN][0]

        from sprites.items.lantern import Lantern

        if isinstance(args.player.get_item(), Lantern):
            source = args.player.get_item()

        self.lights[LIGHT_LAYER_LANTERN].position = source.position

    def draw(self):
        """ Draw light layer """

        if not self.enabled:
            return

        self.light_layer.draw()

    @property
    def enabled(self):
        return self._type is not None

    def enable_layer(self, name):
        if self.lights[name] not in self.light_layer:
            self.light_layer.add(self.lights[name])

    def disable_layer(self, name):
        if self.lights[name] in self.light_layer:
            self.light_layer.remove(self.lights[name])

    def toggle_layer(self, name):
        if self.lights[name] in self.light_layer:
            self.disable_layer()
        else:
            self.enable_layer()
