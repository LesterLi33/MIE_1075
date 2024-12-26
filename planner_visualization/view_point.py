import numpy as np
import argparse

import pygame
from game import Pygame_Window

parser = argparse.ArgumentParser(description="View point location on layout.")
parser.add_argument("-x", type=int, help="x-coordinate of the point")
parser.add_argument("-y", type=int, help="y-coordinate of the point")

args = parser.parse_args()
x_coord = args.x
y_coord = args.y

game = Pygame_Window()

if x_coord < 0  or y_coord < 0:
    raise ValueError("Invalid point coordinates. Values must be greater than 0")
if x_coord > game.width or y_coord > game.height:
    raise ValueError(f"Point coordinate out of bounds. Screen size is {game.size}")

game.add_node((x_coord, y_coord))

while True:
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        game.on_cleanup()