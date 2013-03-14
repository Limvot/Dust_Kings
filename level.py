import os
import random
import pygame
import math
import enemy
from imageAndMapUtil import *

class Level:
	def __init__(self, levelFile, screen, player, difficulity):
		self.levelData = loadConfigFile(levelFile)
		self.tileSize = int(self.levelData["TILE_SIZE_X"]), int(self.levelData["TILE_SIZE_Y"])
		
		levelFileDirectory = os.sep.join(levelFile.split(os.sep)[:-1])
		floorTilesPath = levelFileDirectory + os.sep + self.levelData["FLOOR_TILES"]
		wallTilesPath = levelFileDirectory + os.sep + self.levelData["WALL_TILES"]

		self.wallTiles = parseImage(wallTilesPath, (0,0), self.tileSize, 0, -1, 1)
		self.floorTiles = parseImage(floorTilesPath, (0,0), self.tileSize,0, -1, 1)

		if (self.levelData["DOUBLE_TILE_SIZE"]) == "TRUE":
			self.wallTiles = scaleImageList2x(self.wallTiles)
			self.floorTiles = scaleImageList2x(self.floorTiles)
			self.tileSize = (self.tileSize[0]*2, self.tileSize[1]*2)

		self.sectionSize = (screen.get_size()[0]//self.tileSize[0] + 1,screen.get_size()[1]//self.tileSize[1] + 1)
		self.previousSectionPos = [0,0]
		self.sectionPixelOffset = (0,0)
		self.screenPos = [0,0]

		self.size = ( int(self.levelData["SIZE_X"]), int(self.levelData["SIZE_Y"]))
		
		self.screen = screen
		self.sectionPos = (0,0)			#init some variables

		self.gray = pygame.Surface(screen.get_size())
		self.gray.fill( (185,200,254) )

		self.white = pygame.Surface(self.tileSize)
		self.white.fill( (255,255,255) )

		self.pathWidth = int(self.levelData["PATH_WIDTH"])
		self.mapDict = {}
		self.generateMap()

		self.objects = []
		self.player = player
		self.player.setLevel(self)
		self.player.position = self.beginPosition

		self.difficulity = difficulity

		self.numEnemies = 0

		print("Level " + str(self.difficulity) + "!")

		enemyFileDir = levelFileDirectory + os.sep + self.levelData["ENEMY"]
		self.numEnemies = int(self.levelData["ENEMY_MULTIPLIER"])*self.difficulity
		for i in range(self.numEnemies):
			newPos = (random.randrange(0, self.size[0]), random.randrange(0, self.size[1]))
			while (self.checkGround(newPos)):
				newPos = (random.randint(0, self.size[0]), random.randint(0, self.size[1]))
			newEnemy = enemy.Enemy(enemyFileDir, newPos)
			newEnemy.setLevel(self)
			self.addObject(newEnemy)

	def generatePath(self, position, length, width):
		direction = [0,0]
		direction[random.choice((0,1))] = random.choice([-1,1])

		for i in range(length):
			position = position[0] + direction[0], position[1] + direction[1]
			if position[0]+width >= self.size[0] or position[0]-width <= 0:
				direction[0] = -direction[0]
				position = position[0] + direction[0], position[1] + direction[1]

			if position[1]+width >= self.size[1] or position[1]-width <= 0:
				direction[1] = - direction[1]
				position = position[0] + direction[0], position[1] + direction[1]
			for j in range(-width,width+1):
				for k in range(-width,width+1):	
					self.mapDict[position[0] + j, position[1] + k] = (random.choice(self.floorTiles),0)

			if random.randrange(0,20) == 0:
				direction = [0,0]
				direction[random.choice((0,1))] = random.choice([-1,1])
			if random.randrange(0,self.size[0]*self.size[1]) == 0:
				self.generatePath(position, length-i, width)

	def generateMap(self):
		for i in range(self.size[0]):
			for j in range(self.size[1]):
				self.mapDict[ (i,j) ] = (random.choice(self.wallTiles), 1)

		position = (random.randrange(0,self.size[0]), random.randrange(0,self.size[1]))
		#Used to set the player's position
		self.beginPosition = position
		self.generatePath(position, self.size[0]*self.size[1]//12, self.pathWidth)

	def setScreen(self, screen):
		self.screen = screen

	def addObject(self, obj):
		self.objects.append(obj)

	def remove(self, obj):
		self.objects.remove(obj)

	def checkInBounds(self, obj):
		if obj.position[0] < 0 or obj.position[0] > self.size[0] or obj.position[1] < 0 or obj.position[1] > self.size[1]:
			return(0)
		return(1)

	def checkCollision(self, obj, objRange, excluded):
		#Check for objects in list
		for otherObj in self.objects:
			if otherObj != obj and otherObj != excluded and math.fabs(otherObj.position[0] - obj.position[0]) < objRange and math.fabs(otherObj.position[1] - obj.position[1]) < objRange:
				return(otherObj)
		#Check for player
		if self.player != obj and self.player != excluded and math.fabs(self.player.position[0] - obj.position[0]) < objRange and math.fabs(self.player.position[1] - obj.position[1]) < objRange:
			return(self.player)
		return(0)

	def checkGround(self, position):
		return self.mapDict.get( (math.floor(position[0]), math.floor(position[1]) ), (0,1))[1]

	def update(self, mousePos):
		for obj in self.objects:
			obj.update(self)
		self.player.update(mousePos)

		self.sectionPos = self.player.position[0] - self.sectionSize[0]//2, self.player.position[1] - self.sectionSize[1]//2

		if self.player.alive == False:
			print("Player Dead!!!")

	def getScreenPosition(self, position):
		return ( self.tileSize[0]*(position[0]-self.sectionPos[0]) + self.sectionPixelOffset[0], self.tileSize[1]*(position[1]-self.sectionPos[1]) + self.sectionPixelOffset[1] )


	def draw(self):
		#draw level
		self.screen.blit(self.gray, (0,0) ) #Background
		self.screen.blit(drawMap(self.mapDict, self.tileSize, self.sectionSize, self.sectionPos, self.white), (0,0))	#Draw the new map

		#draw objects
		for obj in self.objects:
			obj.draw(self)
		self.player.draw(self)

		pygame.display.flip()


