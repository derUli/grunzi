def get_layer(name, scene):
    try:
        sprites = scene.get_sprite_list(name)
    except KeyError:
        sprites = []

    return sprites