from sprites.apple import Apple
from sprites.backdrop import Backdrop
from sprites.chainsaw import Chainsaw
from sprites.chicken import Chicken
from sprites.coin import Coin
from sprites.destroyable import Destroyable
from sprites.fence import Fence
from sprites.hammer import Hammer
from sprites.kitten import Kitten
from sprites.levelexit import LevelExit
from sprites.piggybank import PiggyBank
from sprites.sheep import Sheep
from sprites.dog import Dog
from sprites.wall import Wall


def get_editor_blocks(sprites_dir, image_cache):
    """ Get editor blocks array for inline map editor"""
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
            'highway1.jpg'
        ),
        Wall(
            sprites_dir,
            image_cache,
            'shoes.png'
        ),
        Wall(
            sprites_dir,
            image_cache,
            'basket.png'
        ),
        Destroyable(
            sprites_dir,
            image_cache,
            'box.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'rock.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'sand.jpg'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'flower1.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'flower2.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'flower3.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'flower4.png'
        ),
        Backdrop(
            sprites_dir,
            image_cache,
            'flower5.png'
        ),
        Wall(
            sprites_dir,
            image_cache
        ),
        Fence(
            sprites_dir,
            image_cache,
            'wood_fence_horizontal.png'
        ),
        Fence(
            sprites_dir,
            image_cache,
            'wood_fence_vertical.png'
        ),
        Chainsaw(
            sprites_dir,
            image_cache
        ),
        Hammer(
            sprites_dir,
            image_cache
        ),
        Coin(
            sprites_dir,
            image_cache
        ),
        PiggyBank(
            sprites_dir,
            image_cache
        ),
        Apple(
            sprites_dir,
            image_cache
        ),
        Chicken(
            sprites_dir,
            image_cache
        ),
        Kitten(
            sprites_dir,
            image_cache
        ),
        Sheep(
            sprites_dir,
            image_cache
        ),
        Dog(
            sprites_dir,
            image_cache
        ),
        LevelExit(
            sprites_dir,
            image_cache
        )
    ]
