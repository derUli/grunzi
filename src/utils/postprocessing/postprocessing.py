import arcade.sprite
from utils.postprocessing.fog import Fog


class PostProcessing:
    def __init__(self):
        self.pipeline = []
        self.sprite = None

    def setup(self, args):
        self.pipeline = []
        if args.state.difficulty.options['fog']:
            self.pipeline.append(
                Fog().setup(args)
            )

        return self

    def update(self, delta_time, args) -> None:
        for effect in self.pipeline:
            effect.update(delta_time, args)

        w, h = arcade.get_window().get_size()

        if not self.sprite:
            self.sprite = arcade.sprite.SpriteSolidColor(w, h, color=(124, 252, 0, 255))
            self.sprite.alpha = 0

        x, y = args.player.position

        if x < w * 0.5:
            x = w * 0.5

        if y < h * 0.5:
            y = h * 0.5

        self.sprite.position = (x, y)

        import sprites.bullet.slimerbullet
        from constants.layers import LAYER_NPC

        if LAYER_NPC not in args.scene.name_mapping:
            return

        alpha = 0
        radius = h
        max_alpha = 100
        one = max_alpha / radius

        found = False

        for sprite in args.scene[LAYER_NPC]:
            if isinstance(sprite, sprites.bullet.slimerbullet.SlimerBullet):
                distance = arcade.get_distance_between_sprites(sprite, args.player)

                if distance > radius:
                    continue

                found = True

                new_alpha = max_alpha - (one * distance)
                if new_alpha > alpha:
                    alpha = new_alpha

        if alpha > max_alpha:
            alpha = max_alpha

        if not found:
            alpha = self.sprite.alpha - 1

            if alpha < 0:
                alpha = 0

        self.sprite.alpha = alpha


    def draw(self) -> None:
        """ Draw all postprocessing effects """

        for effect in self.pipeline:
            effect.draw()

        if self.sprite:
            self.sprite.draw()
