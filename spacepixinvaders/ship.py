from pygame import *
from spacepixinvaders.config import IMAGES, SCREEN
from random import shuffle, randrange, choice

import sys

class Ship(sprite.Sprite):
	def __init__(self, player_ship):
		sprite.Sprite.__init__(self)
		if not player_ship:
			player_ship = IMAGES['ship']
		self.image = player_ship
		self.rect = self.image.get_rect(topleft=(375, 540))
		self.speed = 5

	def update(self, keys, *args):
		if keys[K_LEFT] and self.rect.x > 10:
			self.rect.x -= self.speed
		if keys[K_RIGHT] and self.rect.x < 740:
			self.rect.x += self.speed
		SCREEN.blit(self.image, self.rect)