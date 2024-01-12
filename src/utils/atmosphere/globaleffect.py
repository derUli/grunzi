class GlobalEffect:

    def __init__(self):
        self.sprites_dir = None
        self.image_cache = None
        self.id = None

    def start(self, args={}, sprites_dir=None, image_cache=None):
        self.sprites_dir = sprites_dir
        self.image_cache = image_cache

    def reset(self):
        pass

    def draw(self, screen):
        pass

    def to_dict(self):
        return {}
