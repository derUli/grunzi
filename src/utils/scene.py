""" Scene utils """
import logging
import time
from typing import Optional, List

import arcade
from arcade import Scene as BaseScene, TileMap
from arcade import SpriteList

from constants.layers import LAYER_NPC
from sprites.characters.character import Character
from sprites.characters.player import Player
from sprites.items.item import Item, Interactable
from sprites.sprite import AbstractSprite, AbstractAnimatedSprite
from utils.lookuptable.lookuptable import LookupTable
from utils.postprocessing.postprocessing import PostProcessing


class Scene(BaseScene):

    def __init__(self):
        """ Constructor """

        super().__init__()
        self.initialized = False
        self.postprocessing = None
        self.args = None
        self.lookup_table = None
        self.measures = []

    def setup(self, args) -> None:
        """ Setup scene """

        self.postprocessing = PostProcessing()
        self.postprocessing.setup(args)
        self.args = args
        self.initialized = True
        self.lookup_table = LookupTable()
        self.setup_sprites(args)

    def setup_sprites(self, args):
        sprites = []

        for sprite_list in self.sprite_lists:
            try:
                filtered = list(filter(
                    lambda x: isinstance(x, AbstractSprite) and not isinstance(x, Player), sprite_list
                ))
                sprites += filtered
            except KeyError:
                continue

        list(map(lambda x: x.setup(args), sprites))

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
        except IndexError:
            pass

        args.player.update_animation()

        if self.postprocessing:
            self.postprocessing.update(delta_time, args)

        self.call_update(delta_time, args)

    def update_animated(self, delta_time, size, scene, player_sprite):
        """ Update animated """

        # Animate only visible
        if self.lookup_table.animated_in_sight.needs_update(player_sprite):
            self.lookup_table.animated_in_sight.set(animated_in_sight(size, scene, player_sprite), player_sprite)

        sprites = self.lookup_table.animated_in_sight.get()

        list(map(lambda sprite: sprite.update_animation(delta_time), sprites))

    def get_collectable(self, player_sprite):
        """ Get collectable item """

        from constants.layers import PASSIVE_LAYERS

        layers = filter(lambda x: x not in PASSIVE_LAYERS, reversed(self.name_mapping))
        layers = map(lambda x: self[x], layers)

        for layer in layers:
            items = filter(lambda x: isinstance(x, Item), layer)

            for item in items:
                if arcade.check_for_collision(player_sprite, item):
                    return item

        return None

    def call_update(self, delta_time, args):
        from constants.layers import STATIC_LAYERS

        layers = filter(lambda x: x not in STATIC_LAYERS, self.name_mapping)
        layers = list(map(lambda x: self[x], layers))

        for layer in layers:
            sprites = filter(lambda x: isinstance(x, AbstractSprite) or isinstance(x, AbstractAnimatedSprite), layer)
            for sprite in sprites:

                a = time.time()
                sprite.update(
                    delta_time,
                    args
                )
                b = time.time() - a

                if b >= 0.01:
                    logging.warning(f"Update sprite {sprite} took too long {b}")

    def make_wall_spritelist(self) -> SpriteList:
        from constants.layers import WALL_LAYERS

        wall_spritelist = SpriteList(lazy=True, use_spatial_hash=True)

        layers = filter(lambda x: x in WALL_LAYERS, self.name_mapping)
        layers = map(lambda x: self[x], layers)

        for layer in layers:
            list(map(lambda x: wall_spritelist.append(x), layer))

        return wall_spritelist

    def draw(self, names: Optional[List[str]] = None, **kwargs):
        self._draw(names=names, **kwargs)

        if self.postprocessing:
            self.postprocessing.draw()

    def _draw(self, names: Optional[List[str]] = None, **kwargs):
        super().draw(names)

        if not self.args:
            return

        from sprites.bullet.bullet import Bullet
        from constants.layers import LAYER_NPC

        try:
            npcs = self[LAYER_NPC]
        except KeyError:
            return

        npcs = filter(
            lambda x: (isinstance(x, Character) or isinstance(x, Bullet)) and
                      self.check_sprite_in_sight(x, self.args.player), npcs)

        list(map(lambda x: x.draw_overlay(self.args), npcs))

    def get_next_sprites(self, distance=150):
        from constants.layers import STATIC_LAYERS

        layers = filter(lambda x: x not in STATIC_LAYERS, reversed(self.name_mapping))
        layers = map(lambda x: self[x], layers)

        found = []

        if not self.args:
            return []

        for layer in layers:
            for sprite in layer:
                dist = arcade.get_distance_between_sprites(self.args.player, sprite)
                if dist < distance:
                    found.append(
                        {
                            'sprite': sprite,
                            'distance': dist
                        }
                    )

        found = sorted(found, key=lambda x: x['distance'], reverse=False)

        return map(lambda x: x['sprite'], found)

    def get_next_interactable(self):
        for sprite in self.get_next_sprites():
            if isinstance(sprite, Interactable):
                return sprite

        return None

    @staticmethod
    def check_sprite_in_sight(sprite1, sprite2, maximum=None):
        w, h = arcade.get_window().get_size()

        if not maximum:
            maximum = h

        return arcade.get_distance_between_sprites(sprite1, sprite2) < maximum

    def cleanup(self):
        for layer in self.name_mapping:
            for sprite in self[layer]:
                if isinstance(sprite, AbstractSprite):
                    sprite.cleanup()

    def kill_all_npcs(self):
        npcs = filter(lambda x: isinstance(x, Character), self[LAYER_NPC])
        for npc in npcs:
            npc.kill()


def animated_in_sight(size, scene, player_sprite) -> list:
    """ Get animated sprites in sight """

    from constants.layers import ANIMATED_LAYERS

    layers = ANIMATED_LAYERS
    animated = []
    update_layers = []

    w, h = size

    cur_frame_idx = {}

    for name in layers:
        cur_frame_idx[name] = 0
        try:
            layer = scene[name]
        except KeyError:
            continue

        for sprite in layer:
            if not isinstance(sprite, arcade.sprite.AnimatedTimeBasedSprite):
                continue

            diff = abs(arcade.get_distance_between_sprites(player_sprite, sprite))

            if diff <= h + sprite.height and sprite.alpha > 0:
                if sprite.cur_frame_idx > cur_frame_idx[name]:
                    cur_frame_idx[name] = sprite.cur_frame_idx

                update_layers.append(name)
                break

    for name in update_layers:
        for sprite in scene[name]:
            sprite.cur_frame_idx = cur_frame_idx[name]
            diff = abs(arcade.get_distance_between_sprites(player_sprite, sprite))

            if diff <= h + sprite.height:
                animated.append(sprite)

    return animated
