import os
import unittest
from arcade import Scene, PymunkPhysicsEngine, SpriteList

from sprites.characters.player import Player
from utils.physics import make_physics_engine


class PhysicsTest(unittest.TestCase):

    def test_make_physics(self):
        image = os.path.join('..', 'src', 'data', 'images', 'sprites', 'char', 'pig.png')
        sprite = Player(image)
        scene = Scene()
        scene.add_sprite_list('Walls', SpriteList())
        scene.add_sprite_list('Moveable', SpriteList())
        self.assertIsInstance(make_physics_engine(sprite, scene), PymunkPhysicsEngine)
