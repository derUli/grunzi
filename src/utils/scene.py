""" Scene utils """
from arcade import Scene, SpriteList


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
