""" Scene utils """
import logging
from typing import Optional, List

import arcade
from arcade import Scene as BaseScene, TileMap
from arcade import SpriteList

from sprites.characters.character import Character
from sprites.items.item import Item, Interactable
from sprites.sprite import AbstractSprite
from utils.lookuptable.lookuptable import LookupTable
from utils.postprocessing.postprocessing import PostProcessing


class Scene(BaseScene):

    def __init__(self):
        """ Constructor """

        super().__init__()
        self.initialized = False
        self.postprocessing = None
        self.args = None
        self.measures = []
        self.lookup_table = None

    def setup(self, args) -> None:
        """ Setup scene """

        self.postprocessing = PostProcessing()
        self.postprocessing.setup(args)
        self.args = args
        self.initialized = True
        self.lookup_table = LookupTable()
        self.setup_sprites(args)

    def setup_sprites(self, args):
        for name in self.name_mapping:
            try:
                for sprite in self[name]:
                    if isinstance(sprite, AbstractSprite) and not isinstance(sprite, Character):
                        sprite.setup(args)
            except KeyError:
                continue

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
        """ Update scene """

        if not self.initialized:
            self.setup(args)

        size = arcade.get_window().get_size()
        try:
            self.update_animated(delta_time, size, self, args.player)
        except IndexError as e:
            logging.error(e)

        if self.postprocessing:
            self.postprocessing.update(delta_time, args)

        self.call_update(delta_time, args)

    def update_animated(self, delta_time, size, scene, player_sprite):
        """ Update animated """

        # Animate only visible
        if self.lookup_table.animated_in_sight.needs_update(player_sprite):
            self.lookup_table.animated_in_sight.set(animated_in_sight(size, scene, player_sprite), player_sprite)

        for sprite in self.lookup_table.animated_in_sight.get():
            sprite.update_animation(delta_time)

    def get_collectable(self, player_sprite):
        """ Get collectable item """

        from constants.layers import PASSIVE_LAYERS

        for layer in reversed(self.name_mapping):
            if layer in PASSIVE_LAYERS:
                continue

            for item in self[layer]:
                if not isinstance(item, Item):
                    continue

                if arcade.check_for_collision(player_sprite, item):
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

    def make_wall_spritelist(self) -> SpriteList:
        from constants.layers import WALL_LAYERS

        wall_spritelist = SpriteList(lazy=True, use_spatial_hash=True)
        for name in WALL_LAYERS:
            layer = get_layer(name, self)

            for item in layer:
                wall_spritelist.append(item)

        return wall_spritelist

    def draw(self, names: Optional[List[str]] = None, **kwargs):
        self._draw(names=names, **kwargs)

        if self.postprocessing:
            self.postprocessing.draw()

    def _draw(self, names: Optional[List[str]] = None, **kwargs):
        from sprites.bullet.bullet import Bullet
        from constants.layers import LAYER_NPC

        super().draw(names)

        for sprite in get_layer(LAYER_NPC, self):
            if not isinstance(sprite, Character) and not isinstance(sprite, Bullet):
                continue

            if self.args and self.check_sprite_in_sight(sprite, self.args.player):
                sprite.draw_overlay(self.args)

    def get_next_sprites(self, distance=200):
        sprites = []
        for sprite_list in self.sprite_lists:
            for sprite in sprite_list:
                if arcade.get_distance_between_sprites(self.args.player, sprite) < distance:
                    sprites.append(sprite)

        return sprites

    def get_next_interactable(self):
        for sprite in self.get_next_sprites():
            if isinstance(sprite, Interactable):
                return sprite

        return None

    def check_sprite_in_sight(self, sprite1, sprite2):
        w, h = arcade.get_window().get_size()

        return arcade.get_distance_between_sprites(sprite1, sprite2) < h


def animated_in_sight(size, scene, player_sprite) -> list:
    """ Get animated sprites in sight """

    from constants.layers import ANIMATED_LAYERS

    layers = ANIMATED_LAYERS
    animated = []

    w, h = size

    cur_frame_idx = {}
    animated = []
    for name in layers:
        cur_frame_idx[name] = 0
        layer = get_layer(name, scene)

        for sprite in layer:

            diff = abs(arcade.get_distance_between_sprites(player_sprite, sprite))

            if diff <= h + sprite.height and sprite.alpha > 0:
                if sprite.cur_frame_idx > cur_frame_idx[name]:
                    cur_frame_idx[name] = sprite.cur_frame_idx

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
