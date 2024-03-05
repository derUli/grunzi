def get_layer(name, scene):
    try:
        sprites = self.scene[LAYER_ENEMIES]
    except KeyError:
        sprites = []

    return sprites