@echo off

game.py --benchmark 30 >> benchmark.txt
game.py --benchmark 60 >> benchmark.txt
game.py --benchmark 120 >> benchmark.txt
game.py --benchmark 180 >> benchmark.txt