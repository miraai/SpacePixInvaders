from spacepixinvaders.blocker import Blocker
from spacepixinvaders.bullet import Bullet
from spacepixinvaders.enemy import Enemy
from spacepixinvaders.explosion import Explosion
from spacepixinvaders.life import Life
from spacepixinvaders.mystery import Mystery
from spacepixinvaders.ship import Ship
from spacepixinvaders.models import HighScore, create_database
from spacepixinvaders.database_gateway import DatabaseGateway
from spacepixinvaders.utils import Text
from spacepixinvaders.config import WHITE, GREEN, PURPLE, RED, BLUE, YELLOW, \
		SCREEN, IMAGES, FONT, DB_PATH

from pygame import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from random import shuffle, randrange, choice
from keyboard import is_pressed
import sys
import os

engine = create_engine(DB_PATH)
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

create_database(Session, engine)

db = DatabaseGateway(session)

#db.insert_player('ajla', 'ship1')
#db.update_score('ajla', 50)
# print(db.show_highscores())

class SpaceInvaders(object):
	def __init__(self):
		mixer.pre_init(44100, -16, 1, 512)
		init()
		self.caption = display.set_caption('Space Pix Invaders')
		self.screen = SCREEN
		self.background = image.load('images/background.jpg').convert()
		self.startGame = False
		self.mainScreen = True
		self.shipScreen = False
		self.gameOver = False
		self.enemyposition = 65

	def reset(self, score, lives, player_ship=None):
		self.player = Ship(player_ship)
		self.playerGroup = sprite.Group(self.player)
		self.explosionsGroup = sprite.Group()
		self.bullets = sprite.Group()
		self.mysteryShip = Mystery()
		self.mysteryGroup = sprite.Group(self.mysteryShip)
		self.enemyBullets = sprite.Group()
		self.reset_lives(player_ship)
		self.make_enemies()
		self.allBlockers = sprite.Group(self.make_blockers(0), self.make_blockers(1), self.make_blockers(2), self.make_blockers(3))
		self.keys = key.get_pressed()
		self.clock = time.Clock()
		self.timer = time.get_ticks()
		self.noteTimer = time.get_ticks()
		self.shipTimer = time.get_ticks()
		self.score = score
		self.lives = lives
		self.create_audio()
		self.create_text()
		self.killedRow = -1
		self.killedColumn = -1
		self.makeNewShip = False
		self.shipAlive = True
		self.killedArray = [[0] * 10 for x in range(5)]

	def make_blockers(self, number):
		blockerGroup = sprite.Group()
		for row in range(4):
			for column in range(9):
				blocker = Blocker(10, GREEN, row, column)
				blocker.rect.x = 50 + (200 * number) + (column * blocker.width)
				blocker.rect.y = 450 + (row * blocker.height)
				blockerGroup.add(blocker)
			return blockerGroup

	def reset_lives(self, player_ship=None):
		self.life1 = Life(715, 3, player_ship)
		self.life2 = Life(742, 3, player_ship)
		self.life3 = Life(769, 3, player_ship)
		self.livesGroup = sprite.Group(self.life1, self.life2, self.life3)
		
	def create_audio(self):
		self.sounds = {}
		for sound_name in ["shoot", "shoot2", "invaderkilled", "mysterykilled", "shipexplosion"]:
			self.sounds[sound_name] = mixer.Sound("sounds/{}.wav".format(sound_name))
			self.sounds[sound_name].set_volume(0.2)

		self.musicNotes = [mixer.Sound("sounds/{}.wav".format(i)) for i in range(4)]
		for sound in self.musicNotes:
			sound.set_volume(0.5)

		self.noteIndex = 0

	def play_main_music(self, currentTime):
		moveTime = self.enemies.sprites()[0].moveTime
		if currentTime - self.noteTimer > moveTime:
			self.note = self.musicNotes[self.noteIndex]
			
			if self.noteIndex < 3:
				self.noteIndex += 1
			else:
				self.noteIndex = 0

			self.note.play()
			self.noteTimer += moveTime

	def create_text(self):
		self.titleText = Text(FONT, 50, "Space Pix Invaders", WHITE, 114, 155)
		self.titleText2 = Text(FONT, 25, "Press any key to continue", WHITE, 201, 225)
		self.pickText = Text(FONT, 40, "Pick your Battleship!", WHITE, 130, 155)
		self.titleText3 = Text(FONT, 25, "Then press any key to continue", WHITE, 150, 225)
		self.gameOverText = Text(FONT, 50, "Game Over", WHITE, 250, 270)
		self.nextRoundText = Text(FONT, 50, "Next Round", WHITE, 240, 270)
		self.enemy1Text = Text(FONT, 25, "   =  10 pts", GREEN, 368, 270)
		self.enemy2Text = Text(FONT, 25, "   =  20 pts", BLUE, 368, 320)
		self.enemy3Text = Text(FONT, 25, "   =  30 pts", PURPLE, 368, 370)
		self.enemy4Text = Text(FONT, 25, "   =  ?????", RED, 368, 420)
		self.ship1Text = Text(FONT, 25, "   =  q", GREEN, 368, 270)
		self.ship2Text = Text(FONT, 25, "   =  w", BLUE, 368, 320)
		self.ship3Text = Text(FONT, 25, "   =  e", PURPLE, 368, 370)
		self.ship4Text = Text(FONT, 25, "   =  r", RED, 368, 420)
		self.scoreText = Text(FONT, 20, "Score", WHITE, 5, 5)
		self.livesText = Text(FONT, 20, "Lives ", WHITE, 640, 5)
		
	def check_input(self):
		self.keys = key.get_pressed()
		for e in event.get():
			if e.type == QUIT:
				sys.exit()
			
			if e.type == KEYDOWN:
				if e.key == K_SPACE:
					if len(self.bullets) == 0 and self.shipAlive:
						if self.score < 1000:
							bullet = Bullet(self.player.rect.x+23, self.player.rect.y+5, -1, 15, "laser", "center")
							self.bullets.add(bullet)
							self.allSprites.add(self.bullets)
							self.sounds["shoot"].play()
						else:
							leftbullet = Bullet(self.player.rect.x+8, self.player.rect.y+5, -1, 15, "laser", "left")
							rightbullet = Bullet(self.player.rect.x+38, self.player.rect.y+5, -1, 15, "laser", "right")
							self.bullets.add(leftbullet)
							self.bullets.add(rightbullet)
							self.allSprites.add(self.bullets)
							self.sounds["shoot2"].play()

	def make_enemies(self):
		enemies = sprite.Group()
		for row in range(5):
			for column in range(10):
				enemy = Enemy(row, column)
				enemy.rect.x = 157 + (column * 50)
				enemy.rect.y = self.enemyposition + (row * 45)
				enemies.add(enemy)
		
		self.enemies = enemies
		self.allSprites = sprite.Group(self.player, self.enemies, self.livesGroup, self.mysteryShip)

	def make_enemies_shoot(self):
		columnList = []
		for enemy in self.enemies:
			columnList.append(enemy.column)

		columnSet = set(columnList)
		columnList = list(columnSet)
		shuffle(columnList)
		column = columnList[0]
		enemyList = []
		rowList = []

		for enemy in self.enemies:
			if enemy.column == column:
				rowList.append(enemy.row)
		
		row = max(rowList)
		
		for enemy in self.enemies:
			if enemy.column == column and enemy.row == row:
				if (time.get_ticks() - self.timer) > 700:
					self.enemyBullets.add(Bullet(enemy.rect.x + 14, enemy.rect.y + 20, 1, 5, "enemylaser", "center"))
					self.allSprites.add(self.enemyBullets)
					self.timer = time.get_ticks() 

	def calculate_score(self, row):
		scores = {0: 30,
				  1: 20,
				  2: 20,
				  3: 10,
				  4: 10,
				  5: choice([50, 100, 150, 300])
				 }
					  
		score = scores[row]
		self.score += score
		
		return score

	def create_main_menu(self):
		self.enemy1 = IMAGES["enemy3_1"]
		self.enemy1 = transform.scale(self.enemy1 , (40, 40))
		self.enemy2 = IMAGES["enemy2_2"]
		self.enemy2 = transform.scale(self.enemy2 , (40, 40))
		self.enemy3 = IMAGES["enemy1_2"]
		self.enemy3 = transform.scale(self.enemy3 , (40, 40))
		self.enemy4 = IMAGES["mystery"]
		self.enemy4 = transform.scale(self.enemy4 , (80, 40))
		self.screen.blit(self.enemy1, (318, 270))
		self.screen.blit(self.enemy2, (318, 320))
		self.screen.blit(self.enemy3, (318, 370))
		self.screen.blit(self.enemy4, (299, 420))

		for e in event.get():
			if e.type == QUIT:
				sys.exit()
			
			if e.type == KEYUP:
				self.shipScreen = True
				self.startGame = False
				self.mainScreen = False

	def choose_ship(self):
		self.ship1 = IMAGES["ship"]
		self.ship1 = transform.scale(self.ship1 , (40, 40))
		self.ship2 = IMAGES["ship1"]
		self.ship2 = transform.scale(self.ship2 , (40, 40))
		self.ship3 = IMAGES["ship2"]
		self.ship3 = transform.scale(self.ship3 , (40, 40))
		self.ship4 = IMAGES["ship3"]
		self.ship4 = transform.scale(self.ship4 , (40, 40))
		self.screen.blit(self.ship1, (318, 270))
		self.screen.blit(self.ship2, (318, 320))
		self.screen.blit(self.ship3, (318, 370))
		self.screen.blit(self.ship4, (318, 420))

		for e in event.get():
			if e.type == QUIT:
				sys.exit()

			if is_pressed('q'):
				self.startGame = True
				self.shipScreen = False
				self.mainScreen = False
				player_ship = self.ship1
			elif is_pressed('w'):
				self.startGame = True
				self.shipScreen = False
				self.mainScreen = False
				player_ship = self.ship2
			elif is_pressed('e'):
				self.startGame = True
				self.shipScreen = False
				self.mainScreen = False
				player_ship = self.ship3
			elif is_pressed('r'):
				self.startGame = True
				self.shipScreen = False
				self.mainScreen = False
				player_ship = self.ship4
			else:
				player_ship = self.ship1
			db.insert_player('Ajla')
			return player_ship

	def update_enemy_speed(self):
		if len(self.enemies) <= 10:
			for enemy in self.enemies:
				enemy.moveTime = 400
		
		if len(self.enemies) == 1:
			for enemy in self.enemies:
				enemy.moveTime = 200
				
	def check_collisions(self, player_ship=None):
		collidedict = sprite.groupcollide(self.bullets, self.enemyBullets, True, False)
		if collidedict:
			for value in collidedict.values():
				for currentSprite in value:
					self.enemyBullets.remove(currentSprite)
					self.allSprites.remove(currentSprite)

		enemiesdict = sprite.groupcollide(self.bullets, self.enemies, True, False)
		if enemiesdict:
			for value in enemiesdict.values():
				for currentSprite in value:
					self.sounds["invaderkilled"].play()
					self.killedRow = currentSprite.row
					self.killedColumn = currentSprite.column
					score = self.calculate_score(currentSprite.row)
					explosion = Explosion(currentSprite.rect.x, currentSprite.rect.y, currentSprite.row, False, False, score, player_ship)
					self.explosionsGroup.add(explosion)
					self.allSprites.remove(currentSprite)
					self.enemies.remove(currentSprite)
					self.gameTimer = time.get_ticks()
					break
		
		mysterydict = sprite.groupcollide(self.bullets, self.mysteryGroup, True, True)
		if mysterydict:
			for value in mysterydict.values():
				for currentSprite in value:
					currentSprite.mysteryEntered.stop()
					self.sounds["mysterykilled"].play()
					score = self.calculate_score(currentSprite.row)
					explosion = Explosion(currentSprite.rect.x, currentSprite.rect.y, currentSprite.row, False, True, score, player_ship)
					self.explosionsGroup.add(explosion)
					self.allSprites.remove(currentSprite)
					self.mysteryGroup.remove(currentSprite)
					newShip = Mystery()
					self.allSprites.add(newShip)
					self.mysteryGroup.add(newShip)
					break

		bulletsdict = sprite.groupcollide(self.enemyBullets, self.playerGroup, True, False)     
		if bulletsdict:
			for value in bulletsdict.values():
				for playerShip in value:
					if self.lives == 3:
						self.lives -= 1
						self.livesGroup.remove(self.life3)
						self.allSprites.remove(self.life3)
					elif self.lives == 2:
						self.lives -= 1
						self.livesGroup.remove(self.life2)
						self.allSprites.remove(self.life2)
					elif self.lives == 1:
						self.lives -= 1
						self.livesGroup.remove(self.life1)
						self.allSprites.remove(self.life1)
					elif self.lives == 0:
						self.gameOver = True
						self.startGame = False
					self.sounds["shipexplosion"].play()
					explosion = Explosion(playerShip.rect.x, playerShip.rect.y, 0, True, False, 0, player_ship)
					self.explosionsGroup.add(explosion)
					self.allSprites.remove(playerShip)
					self.playerGroup.remove(playerShip)
					self.makeNewShip = True
					self.shipTimer = time.get_ticks()
					self.shipAlive = False

		if sprite.groupcollide(self.enemies, self.playerGroup, True, True):
			self.gameOver = True
			self.startGame = False

		sprite.groupcollide(self.bullets, self.allBlockers, True, True)
		sprite.groupcollide(self.enemyBullets, self.allBlockers, True, True)
		sprite.groupcollide(self.enemies, self.allBlockers, False, True)

	def create_new_ship(self, createShip, currentTime, player_ship):
		if createShip and (currentTime - self.shipTimer > 900):
			self.player = Ship(player_ship)
			self.allSprites.add(self.player)
			self.playerGroup.add(self.player)
			self.makeNewShip = False
			self.shipAlive = True

	def create_game_over(self, currentTime):
		self.screen.blit(self.background, (0,0))
		if currentTime - self.timer < 750:
			self.gameOverText.draw(self.screen)
		if currentTime - self.timer > 750 and currentTime - self.timer < 1500:
			self.screen.blit(self.background, (0,0))
		if currentTime - self.timer > 1500 and currentTime - self.timer < 2250:
			self.gameOverText.draw(self.screen)
		if currentTime - self.timer > 2250 and currentTime - self.timer < 2750:
			self.screen.blit(self.background, (0,0))
		if currentTime - self.timer > 3000:
			self.mainScreen = True
		
		for e in event.get():
			if e.type == QUIT:
				sys.exit()

	def main(self):
		while True:
			if self.mainScreen:
				self.reset(0, 3)
				self.screen.blit(self.background, (0,0))
				self.titleText.draw(self.screen)
				self.titleText2.draw(self.screen)
				self.enemy1Text.draw(self.screen)
				self.enemy2Text.draw(self.screen)
				self.enemy3Text.draw(self.screen)
				self.enemy4Text.draw(self.screen)
				self.create_main_menu()
			
			elif self.shipScreen:
				self.screen.blit(self.background, (0,0))
				self.pickText.draw(self.screen)
				self.titleText3.draw(self.screen)
				self.ship1Text.draw(self.screen)
				self.ship2Text.draw(self.screen)
				self.ship3Text.draw(self.screen)
				self.ship4Text.draw(self.screen)
				player_ship = self.choose_ship()
				
				self.reset(0, 3, player_ship)

			elif self.startGame:
				if len(self.enemies) == 0:
					currentTime = time.get_ticks()
					
					if currentTime - self.gameTimer < 3000:              
						self.screen.blit(self.background, (0,0))
						self.scoreText2 = Text(FONT, 20, str(self.score), GREEN, 85, 5)
						self.scoreText.draw(self.screen)
						self.scoreText2.draw(self.screen)
						self.nextRoundText.draw(self.screen)
						self.livesText.draw(self.screen)
						self.livesGroup.update(self.keys)
						self.check_input()
					
					if currentTime - self.gameTimer > 3000:
						self.reset(self.score, self.lives, player_ship)
						self.enemyposition += 35
						self.make_enemies()
						self.gameTimer += 3000
				else:
					currentTime = time.get_ticks()
					self.play_main_music(currentTime)              
					self.screen.blit(self.background, (0,0))
					self.allBlockers.update(self.screen)
					self.scoreText2 = Text(FONT, 20, str(self.score), GREEN, 85, 5)
					self.scoreText.draw(self.screen)
					self.scoreText2.draw(self.screen)
					self.livesText.draw(self.screen)
					self.check_input()
					self.allSprites.update(self.keys, currentTime, self.killedRow, self.killedColumn, self.killedArray)
					self.explosionsGroup.update(self.keys, currentTime)
					self.check_collisions(player_ship)
					self.create_new_ship(self.makeNewShip, currentTime, player_ship)
					self.update_enemy_speed()

					if len(self.enemies) > 0:
						self.make_enemies_shoot()
	
			elif self.gameOver:
				currentTime = time.get_ticks()
				db.update_score('Ajla', self.score)
				self.create_game_over(currentTime)

			display.update()
			self.clock.tick(60)