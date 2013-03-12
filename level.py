import os
import pygame
from imageAndMapUtil import *

class Level:
	def __init__(self, levelFile, screen, player):
		self.levelData = loadConfigFile(levelFile)
		self.tileSize = int(self.levelData["TILE_SIZE_X"]), int(self.levelData["TILE_SIZE_Y"])
		levelFileDirectory = os.sep.join(levelFile.split(os.sep)[:-1])
		mapImgDir = levelFileDirectory + os.sep + self.levelData["LEVEL_GRID_IMAGE"]
		mapPickDir = levelFileDirectory + os.sep + self.levelData["LEVEL_LAYOUT_PICKLE"]
		self.mapDict, self.tileList = loadMap(mapImgDir, mapPickDir, self.tileSize)
		
		self.screen = screen

		self.objects = []
		self.player = player

		self.sectionPos = (0,0)			#init some variables
		self.sectionSize = (screen.get_size()[0]//self.tileSize[0],screen.get_size()[1]//self.tileSize[1])
		self.previousSectionPos = [0,0]
		self.sectionPixelOffset = (0,0)
		self.screenPos = [0,0]

		self.gray = pygame.Surface(screen.get_size())
		self.gray.fill( (185,200,254) )

	def setScreen(self, screen):
		self.screen = screen

	def addObject(self, obj):
		self.objects.append(obj)

	def remove(self, obj):
		self.objects.remove(obj)

	def checkInBounds(self, obj):
		if obj.position[0] < 0 or obj.position[0] > self.width or obj.position[1] < 0 or obj.position[1] > self.hight:
			return 0
		return 1

	def checkCollision(self, obj, objRange):
		#Check for objects in list
		for otherObj in self.objects:
			if otherObj != obj and otherObj.position[0] - obj.position[0] < objRange and otherObj.position[1] - obj.position[1] < objRange:
					return 1
		#Check for player
		if self.player != obj and self.player.position[0] - obj.position[0] < objRange and self.player.position[1] - obj.position[1] < objRange:
			return 1
		return 0

	def update(self, mousePos):
		for obj in self.objects:
			obj.update()
		self.player.update(mousePos)

		self.sectionPos = self.player.position[0] - self.sectionSize[0]//2, self.player.position[1] - self.sectionSize[1]//2

	def getScreenPosition(self, position):
		return ( self.tileSize[0]*(position[0]-self.sectionPos[0]) + self.sectionPixelOffset[0], self.tileSize[1]*(position[1]-self.sectionPos[1]) + self.sectionPixelOffset[1] )


	def draw(self):
		#draw level
		self.screen.blit(self.gray, (0,0) ) #Background
		self.screen.blit(drawMap(self.mapDict, self.tileList, self.tileSize, self.sectionSize, self.sectionPos), (0,0))	#Draw the new map

		#draw objects
		for obj in self.objects:
			obj.draw(self)
		self.player.draw(self)

		pygame.display.flip()


