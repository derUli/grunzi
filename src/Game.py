""" Grunzi Game Launcher """
import os
from bootstrap.gamecontainer import GameContainer

root_dir = os.path.join(os.path.dirname(__file__))

game = GameContainer(root_dir)
game.start()
