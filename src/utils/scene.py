""" Scene utils """
from arcade import Scene, SpriteList


def get_layer(name: str, scene: Scene) -> SpriteList:
    """
    Get layer from scene
    @param name: Name of layer
    @param scene: Scene
    @return: List of sprites
    """

    sprites = SpriteList()
    if name in scene.name_mapping:
        sprites = scene[name]

    return sprites
