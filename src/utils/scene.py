""" Scene utils """
import random

from arcade import Scene as BaseScene, TileMap
from arcade import SpriteList


class Scene(BaseScene):

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

    def update_scene(self, state, scene, tilemap, physics_engine):
        self.update_enemies(state, scene, tilemap, physics_engine)

    def update_enemies(self, state, scene, tilemap, physics_engine):
        from constants.layers import LAYER_NPC
        from sprites.characters.skull import spawn_skull

        enemies = get_layer(LAYER_NPC, scene)

        if len(enemies) < state.difficulty.max_skulls:
            a, b = state.difficulty.skull_spawn_range
            if random.randint(a, b) == 50:
                spawn_skull(state, tilemap.map, scene, physics_engine)

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
