from pygame import *
from spacepixinvaders.config import IMAGES, SCREEN
from random import shuffle, randrange, choice

import sys

class Mystery(sprite.Sprite):
	def __init__(self):
		sprite.Sprite.__init__(self)
		self.image = IMAGES["mystery"]
		self.image = transform.scale(self.image, (75, 35))
		self.rect = self.image.get_rect(topleft=(-80, 45))
		self.row = 5
		self.moveTime = 25000
		self.direction = 1
		self.timer = time.get_ticks()
		self.mysteryEntered = mixer.Sound('sounds/mysteryentered.wav')
		self.mysteryEntered.set_volume(0.3)
		self.playSound = True

	def update(self, keys, currentTime, *args):
		resetTimer = False
		if (currentTime - self.timer > self.moveTime) and (self.rect.x < 0 or self.rect.x > 800) and self.playSound:
			self.mysteryEntered.play()
			self.playSound = False
		
		if (currentTime - self.timer > self.moveTime) and self.rect.x < 840 and self.direction == 1:
			self.mysteryEntered.fadeout(4000)
			self.rect.x += 2
			SCREEN.blit(self.image, self.rect)
		
		if (currentTime - self.timer > self.moveTime) and self.rect.x > -100 and self.direction == -1:
			self.mysteryEntered.fadeout(4000)
			self.rect.x -= 2
			SCREEN.blit(self.image, self.rect)
		
		if (self.rect.x > 830):
			self.playSound = True
			self.direction = -1
			resetTimer = True
		
		if (self.rect.x < -90):
			self.playSound = True
			self.direction = 1
			resetTimer = True
		
		if (currentTime - self.timer > self.moveTime) and resetTimer:
			self.timer = currentTime