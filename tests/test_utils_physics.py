import os
import unittest

import arcade.sprite
from arcade import Scene, PymunkPhysicsEngine, SpriteList

from sprites.characters.player import Player
from utils.physics import make_physics_engine, on_hit_destroy


class PhysicsTest(unittest.TestCase):

    def test_make_physics(self):
        image = os.path.join('..', 'src', 'data', 'images', 'sprites', 'char', 'pig', 'default.png')
        sprite = Player(image)
        scene = Scene()
        scene.add_sprite_list('Walls', SpriteList())
        scene.add_sprite_list('Moveable', SpriteList())
        self.assertIsInstance(make_physics_engine(sprite, scene), PymunkPhysicsEngine)

    def test_on_hit_destroy(self):
        sprites = SpriteList()

        sprites.append(
            arcade.sprite.SpriteSolidColor(color=arcade.color.RED, width=60, height=60)
        )

        on_hit_destroy(sprites[0], None, None, None, None)

        self.assertEqual(len(sprites), 0)
