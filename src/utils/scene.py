""" Scene utils """
from typing import Optional, List

import arcade
from arcade import Scene as BaseScene, TileMap
from arcade import SpriteList
from arcade.experimental.lights import LightLayer, Light

from sprites.characters.character import Character
from sprites.items.item import Item
from sprites.sprite import AbstractSprite


class Scene(BaseScene):

    def __init__(self):
        super().__init__()

        self.light_layer = None
        self.player_light = None
        self.initialized = False

    def setup(self, args):
        # TODO: implement LightManager
        w, h = arcade.get_window().get_size()

        self.light_layer = LightLayer(w, h)
        # We can also set the background color that will be lit by lights,
        # but in this instance we just want a black background
        self.light_layer.set_background_color(arcade.color.BLACK)

        # Create a light to follow the player around.
        # We'll position it later, when the player moves.
        # We'll only add it to the light layer when the player turns the light
        # on. We start with the light off.
        radius = w * 2
        mode = 'hard'
        color = arcade.csscolor.WHITE
        self.player_light = Light(args.player.center_x, args.player.center_y, radius, color, mode)

        self.light_layer.add(self.player_light)

        self.initialized = True

    @classmethod
    def from_tilemap(cls, tilemap: TileMap) -> "Scene":
        """
        Create a new Scene from a `TileMap` object.

        This will look at all the SpriteLists in a TileMap object and create
        a Scene with them. This will automatically keep SpriteLists in the same
        order as they are defined in the TileMap class, which is the order that
        they are defined within Tiled.

        :param TileMap tilemap: The `TileMap` object to create the scene from.
        """
        scene = cls()
        for name, sprite_list in tilemap.sprite_lists.items():
            scene.add_sprite_list(name=name, sprite_list=sprite_list)
        return scene

    def update_scene(self, delta_time, args):
        # if not self.initialized:
        # self.setup(args)

        # self.player_light.position = args.player.position

        size = arcade.get_window().get_size()
        self.update_animated(delta_time, size, self, args.player)
        self.call_update(delta_time, args)

    def update_animated(self, delta_time, size, scene, player_sprite):
        # Animate only visible
        animated = animated_in_sight(size, scene, player_sprite)
        for sprite in animated:
            sprite.update_animation(delta_time)

    def get_collectable(self, player_sprite):
        items = arcade.check_for_collision_with_lists(player_sprite, self.sprite_lists)

        for item in reversed(items):
            if isinstance(item, Item):
                return item

        return None

    def call_update(self, delta_time, args):

        for sprite_list in args.scene.sprite_lists:
            for sprite in sprite_list:

                if not isinstance(sprite, AbstractSprite):
                    continue

                sprite.update(
                    delta_time,
                    args
                )

    def make_wall_spritelist(self):
        from constants.layers import WALL_LAYERS

        wall_spritelist = SpriteList(lazy=True, use_spatial_hash=True)
        for name in WALL_LAYERS:
            layer = get_layer(name, self)

            for item in layer:
                wall_spritelist.append(item)

        return wall_spritelist

    def draw(self, names: Optional[List[str]] = None, **kwargs):
        if not self.light_layer:
            self._draw(names=names, **kwargs)
            return

        with self.light_layer:
            self._draw(names=names, **kwargs)

        self.light_layer.draw()

    def _draw(self, names: Optional[List[str]] = None, **kwargs):
        from sprites.bullet.bullet import Bullet
        from constants.layers import LAYER_NPC

        super().draw(names)

        for sprite in get_layer(LAYER_NPC, self):

            if not isinstance(sprite, Character) and not isinstance(sprite, Bullet):
                continue

            sprite.draw_overlay()


def animated_in_sight(size, scene, player_sprite) -> list:
    """ Get animated sprites in sight """

    from constants.layers import ANIMATED_LAYERS

    layers = ANIMATED_LAYERS

    animated = []

    for name in layers:
        layer = get_layer(name, scene)
        for sprite in layer:
            w, h = size

            diff = abs(arcade.get_distance_between_sprites(player_sprite, sprite))
            if diff <= h:
                animated.append(sprite)

    return animated


def get_layer(name: str, scene: Scene) -> SpriteList:
    """
    Get layer from scene
    @param name: Name of layer
    @param scene: Scene
    @return: List of sprites
    """

    if name in scene.name_mapping:
        return scene[name]

    return SpriteList(use_spatial_hash=True)
