from sprites.backdrop import Backdrop
def get_editor_blocks(sprites_dir, image_cache):
    return [
        Backdrop(
            sprites_dir,
            image_cache,
            'placeholder.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'gras1.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'gras2.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'gras3.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'pebble.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'sand.jpg'
        )
    ]
