import unittest
import os

from arcade import Scene, PymunkPhysicsEngine, SpriteList

from sprites.characters.playersprite import PlayerSprite
from utils.physics import make_physics_engine
from utils.screenshot import make_screenshot
from views.mainmenu import MainMenu

class PhysicsTest(unittest.TestCase):

    def test_make_physics(self):

        image = os.path.join('..', 'src', 'data', 'images', 'sprites', 'pig.png')
        sprite = PlayerSprite(image)
        scene = Scene()
        scene.add_sprite_list('Walls', SpriteList())
        scene.add_sprite_list('Moveable', SpriteList())
        self.assertIsInstance(make_physics_engine(sprite, scene), PymunkPhysicsEngine)