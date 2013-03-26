import math
import copy
import person
from imageAndMapUtil import *

class Pickup:
	def __init__(self, pickupFile, position, level):

		self.config = loadConfigFile(pickupFile)

		self.position = position

		pickupFileDirectory = justDir(pickupFile)
		tileListDir = pickupFileDirectory + os.sep + self.config["TILES"]
		self.tileList = parseImage(tileListDir, (0,0), (int(self.config["TILE_END_X"]),int(self.config["TILE_END_Y"])), 0, -1, 1)

		self.size = int(self.config["SIZE"])

		self.framesPerSprite = int(self.config["FRAMES_PER_SPRITE"])

		self.addHealth = int(self.config.get("HEALTH", 0) )

		self.addAmmoType, self.addAmmoAmmount = self.config.get("AMMO", (0,0))
		#Remove file extension from ammo type
		if self.addAmmoType != 0:
			self.addAmmoType = self.addAmmoType.split(".")[-2]
			self.addAmmoAmmount = int(self.addAmmoAmmount)

		self.whichStep = 0

		self.hasBeenPickedUp = False

	def clone(self):
		return(copy.copy(self))

	def setPosition(self, position):
		self.position = position

	def update(self, level):
		self.collide(level)

	def collide(self, level):
		#Don't really have any to avoid collision with, so just pass self again
		for collidee in level.checkCollision(self, self.size, self):
			if collidee == level.player:
				if not self.hasBeenPickedUp:
					self.bePickedUp(level)

	def bePickedUp(self, level):
		self.hasBeenPickedUp = True
		level.player.addHealth(self.addHealth)
		if self.addAmmoAmmount != 0:
			level.player.addAmmo(self.addAmmoType, self.addAmmoAmmount)
		level.remove(self)

	#projectiles don't matter
	def collideWithProjectile(self, projectile, level):
		return(False)

	def getCurrentSprite(self):
		self.whichStep += 1
		if self.whichStep >= len(self.tileList)*self.framesPerSprite:
			self.whichStep = 0

		return(self.tileList[self.whichStep//self.framesPerSprite])

	def draw(self, level):
		#Draw so that position is center of object
		sprite = self.getCurrentSprite()
		levelPos = level.getScreenPosition(self.position)
		drawPos = levelPos[0]-sprite.get_width()//2,levelPos[1]-sprite.get_height()//2
		level.screen.blit(sprite, drawPos)