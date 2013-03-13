import os
import random
import pygame
import math
import enemy
from imageAndMapUtil import *

class Level:
	def __init__(self, levelFile, screen, player):
		self.levelData = loadConfigFile(levelFile)
		self.tileSize = int(self.levelData["TILE_SIZE_X"]), int(self.levelData["TILE_SIZE_Y"])
		
		levelFileDirectory = os.sep.join(levelFile.split(os.sep)[:-1])
		floorTilesDir = levelFileDirectory + os.sep + self.levelData["FLOOR_TILES"]
		wallTilesDir = levelFileDirectory + os.sep + self.levelData["WALL_TILES"]

		self.size = ( int(self.levelData["SIZE_X"]), int(self.levelData["SIZE_Y"]))
		
		self.screen = screen
		self.sectionPos = (0,0)			#init some variables
		self.sectionSize = (screen.get_size()[0]//self.tileSize[0] + 1,screen.get_size()[1]//self.tileSize[1] + 1)
		self.previousSectionPos = [0,0]
		self.sectionPixelOffset = (0,0)
		self.screenPos = [0,0]

		self.gray = pygame.Surface(screen.get_size())
		self.gray.fill( (185,200,254) )

		self.white = pygame.Surface(self.tileSize)
		self.white.fill( (255,255,255) )

		self.mapDict = {}
		self.generateMap(floorTilesDir, wallTilesDir)

		self.objects = []
		self.player = player
		self.player.position = self.beginPosition

		enemyFileDir = levelFileDirectory + os.sep + self.levelData["ENEMY"]
		for i in range(int(self.levelData["ENEMY_MULTIPLIER"])):
			newPos = (random.randint(0, self.size[0]), random.randint(0, self.size[1]))
			while (self.checkGround(newPos)):
				newPos = (random.randint(0, self.size[0]), random.randint(0, self.size[1]))
			newEnemy = enemy.Enemy(enemyFileDir, newPos)
			newEnemy.setLevel(self)
			self.addObject(newEnemy)




	def generatePath(self, position, floorTiles, length):
		direction = [0,0]
		direction[random.choice((0,1))] = random.choice([-1,1])

		for i in range(length):
			position = position[0] + direction[0], position[1] + direction[1]
			if position[0] < 0 or position[0] > self.size[0]:
				direction[0] = -direction[0]

			if position[1] < 0 or position[1] > self.size[1]:
				direction[1] = - direction[1]
			for j in range(-4,5):
				for k in range(-4,5):	
					self.mapDict[position[0] + j, position[1] + j] = (random.choice(floorTiles),0)

			if random.randint(0,20) == 0:
				direction = [0,0]
				direction[random.choice((0,1))] = random.choice([-1,1])
			if random.randint(0,self.size[0]*self.size[1]) == 0:
				self.generatePath(position, floorTiles, length-i)

	def generateMap(self, floorTilesPath, wallTilesPath):

		wallTiles = parseImage(wallTilesPath, (0,0), self.tileSize, 0, -1, 1)
		floorTiles = parseImage(floorTilesPath, (0,0), self.tileSize,0, -1, 1)

		for i in range(self.size[0]):
			for j in range(self.size[1]):
				self.mapDict[ (i,j) ] = (random.choice(wallTiles), 1)

		position = (random.randint(0,self.size[0]), random.randint(0,self.size[1]))
		#Used to set the player's position
		self.beginPosition = position
		self.generatePath(position, floorTiles, self.size[0]*self.size[1]//12)


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
			if otherObj != obj and otherObj != excluded and otherObj.position[0] - obj.position[0] < objRange and otherObj.position[1] - obj.position[1] < objRange:
					return(otherObj)
		#Check for player
		if self.player != obj and self.player != excluded and self.player.position[0] - obj.position[0] < objRange and self.player.position[1] - obj.position[1] < objRange:
			return(self.player)
		return(0)

	def checkGround(self, position):

		return self.mapDict.get( (math.floor(position[0]), math.floor(position[1]) ), (0,0))[1]

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


