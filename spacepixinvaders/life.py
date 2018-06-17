from pygame import *
from spacepixinvaders.config import IMAGES, SCREEN
from random import shuffle, randrange, choice

import sys

class Life(sprite.Sprite):
	def __init__(self, xpos, ypos, player_ship):
		sprite.Sprite.__init__(self)
		if not player_ship:
			player_ship = IMAGES['ship']
		self.image = player_ship
		self.image = transform.scale(self.image, (23, 23))
		self.rect = self.image.get_rect(topleft=(xpos, ypos))
		
	def update(self, keys, *args):
		SCREEN.blit(self.image, self.rect)