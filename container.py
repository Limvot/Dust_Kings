import math
import copy
import person
from imageAndMapUtil import *

class Container:
	def __init__(self, containerFile, position, contentsConfigFile, contentsConstructor):

		self.contentsConfigFile = contentsConfigFile
		self.contentsConstructor = contentsConstructor

		self.config = loadConfigFile(containerFile)

		self.position = position

		containerFileDirectory = justDir(containerFile)
		closedTileListDir = containerFileDirectory + os.sep + self.config["CLOSED_TILES"]
		self.closedTiles = parseImage(closedTileListDir, (0,0), (int(self.config["TILE_END_X"]),int(self.config["TILE_END_Y"])), 0, -1, 1)

		openTileListDir = containerFileDirectory + os.sep + self.config["OPEN_TILES"]
		self.openTiles = parseImage(openTileListDir, (0,0), (int(self.config["TILE_END_X"]),int(self.config["TILE_END_Y"])), 0, -1, 1)

		self.size = int(self.config["SIZE"])

		self.framesPerSprite = int(self.config["FRAMES_PER_SPRITE"])

		self.whichStep = 0

		self.isOpen = False

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
				if not self.isOpen:
					self.open(level)

	def open(self, level):
		self.isOpen = True
		#By convention, stuff spawned from chests has level as its owner
		level.addObject(self.contentsConstructor(self.contentsConfigFile, self.position, level))

	#projectiles don't matter
	def collideWithProjectile(self, projectile, level):
		return(False)

	def getCurrentSprite(self):
		if self.isOpen:
			tileList = self.openTiles
		else:
			tileList = self.closedTiles

		self.whichStep += 1
		if self.whichStep >= len(tileList)*self.framesPerSprite:
			self.whichStep = 0

		return(tileList[self.whichStep//self.framesPerSprite])

	def draw(self, level):
		level.screen.blit(self.getCurrentSprite(), level.getScreenPosition(self.position))


