from pygame import *
import sys
from random import shuffle, randrange, choice

# Colours
WHITE = (255, 255, 255)
GREEN = (78, 255, 87)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)
RED = (237, 28, 36)

SCREEN = display.set_mode((800,600))

FONT = "fonts/space_invaders.ttf"
IMG_NAMES = ["ship", "ship", "mystery", "enemy1_1", "enemy1_2", "enemy2_1", "enemy2_2",
				"enemy3_1", "enemy3_2", "explosionblue", "explosiongreen", "explosionpurple", "laser", "enemylaser"]
IMAGES = {name: image.load("images/{}.png".format(name)).convert_alpha()
				for name in IMG_NAMES}

