from pygame import *
from spacepixinvaders.config import IMAGES, SCREEN, FONT, WHITE, GREEN, YELLOW, BLUE, PURPLE, RED
from random import shuffle, randrange, choice
from spacepixinvaders.utils import Text

import sys

class Explosion(sprite.Sprite):
	def __init__(self, xpos, ypos, row, ship, mystery, score, player_ship):
		sprite.Sprite.__init__(self)
		self.isMystery = mystery
		self.isShip = ship
		
		if mystery:
			self.text = Text(FONT, 20, str(score), WHITE, xpos+20, ypos+6)
		elif ship:
			if not player_ship:
				player_ship = IMAGES['ship']
			self.image = player_ship
			self.rect = self.image.get_rect(topleft=(xpos, ypos))
		else:
			self.row = row
			self.load_image()
			self.image = transform.scale(self.image, (40, 35))
			self.rect = self.image.get_rect(topleft=(xpos, ypos))
			SCREEN.blit(self.image, self.rect)
			
		self.timer = time.get_ticks()
		
	def update(self, keys, currentTime):
		if self.isMystery:
			if currentTime - self.timer <= 200:
				self.text.draw(SCREEN)
			
			if currentTime - self.timer > 400 and currentTime - self.timer <= 600:
				self.text.draw(SCREEN)
			
			if currentTime - self.timer > 600:
				self.kill()
		elif self.isShip:
			if currentTime - self.timer > 300 and currentTime - self.timer <= 600:
				SCREEN.blit(self.image, self.rect)
		
			if currentTime - self.timer > 900:
				self.kill()
		else:
			if currentTime - self.timer <= 100:
				SCREEN.blit(self.image, self.rect)
		
			if currentTime - self.timer > 100 and currentTime - self.timer <= 200:
				self.image = transform.scale(self.image, (50, 45))
				SCREEN.blit(self.image, (self.rect.x-6, self.rect.y-6))
		
			if currentTime - self.timer > 400:
				self.kill()
	
	def load_image(self):
		imgColors = ["purple", "blue", "blue", "green", "green"]
		self.image = IMAGES["explosion{}".format(imgColors[self.row])]