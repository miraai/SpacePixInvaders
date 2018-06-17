from pygame import *
from spacepixinvaders.config import IMAGES, SCREEN
from random import shuffle, randrange, choice

import sys

class Life(sprite.Sprite):
	def __init__(self, xpos, ypos):
		sprite.Sprite.__init__(self)
		self.image = IMAGES["ship"]
		self.image = transform.scale(self.image, (23, 23))
		self.rect = self.image.get_rect(topleft=(xpos, ypos))
		
	def update(self, keys, *args):
		SCREEN.blit(self.image, self.rect)