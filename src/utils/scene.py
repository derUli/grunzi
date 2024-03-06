""" Scene utils """
from arcade import Scene, SpriteList


def get_layer(name: str, scene: Scene) -> SpriteList:
    """
    Get layer from scene
    @param name: Name of layer
    @param scene: Scene
    @return: List of sprites
    """
    try:
        sprites = scene.get_sprite_list(name)
    except KeyError:
        sprites = SpriteList()

    return sprites
