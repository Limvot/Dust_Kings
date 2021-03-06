import os
import random
import pygame
import copy
import math
import enemy
import projectile
import weapon
import container
import pickup
from imageAndMapUtil import *

class Level:
	def __init__(self, levelFile, screen, player, difficulity):
		self.levelData = loadConfigFile(levelFile)
		self.tileSize = int(self.levelData["TILE_SIZE_X"]), int(self.levelData["TILE_SIZE_Y"])
		
		self.levelFileDirectory = justDir(levelFile)
		floorTilesPath = self.levelFileDirectory + os.sep + self.levelData["FLOOR_TILES"]
		wallTilesPath = self.levelFileDirectory + os.sep + self.levelData["WALL_TILES"]

		self.wallTiles = parseImage(wallTilesPath, (0,0), self.tileSize, 0, -1, 1)
		self.wallTiles = self.distribute(self.wallTiles)
		self.floorTiles = parseImage(floorTilesPath, (0,0), self.tileSize,0, -1, 1)
		self.floorTiles = self.distribute(self.floorTiles)

		outOfBoundsStringList = self.levelData["OUT_OF_BOUNDS_COLOR"]
		self.outOfBoundsTile = pygame.Surface(self.tileSize)
		self.outOfBoundsTile.fill( (int(outOfBoundsStringList[0]),int(outOfBoundsStringList[1]),int(outOfBoundsStringList[2])) )
		self.outOfBoundsSurface = pygame.Surface(screen.get_size())
		self.outOfBoundsSurface.fill( (int(outOfBoundsStringList[0]),int(outOfBoundsStringList[1]),int(outOfBoundsStringList[2])) )

		if (self.levelData["DOUBLE_TILE_SIZE"]) == "TRUE":
			self.wallTiles = scaleImageList2x(self.wallTiles)
			self.floorTiles = scaleImageList2x(self.floorTiles)
			self.tileSize = (self.tileSize[0]*2, self.tileSize[1]*2)

		self.sectionSize = (screen.get_size()[0]//self.tileSize[0] + 1,screen.get_size()[1]//self.tileSize[1] + 1)
		self.previousSectionPos = [0,0]
		self.sectionPixelOffset = (0,0)
		self.screenPos = [0,0]
		self.recoilOffset = (0,0)

		self.size = ( int(self.levelData["SIZE_X"]), int(self.levelData["SIZE_Y"]))
		
		self.screen = screen
		self.sectionPos = (0,0)			#init some variables

		self.pathWidth = int(self.levelData["PATH_WIDTH"])
		self.mapDict = {}
		self.generateMap()

		self.objects = []
		self.objectsToRemove = []
		self.player = player
		self.player.setLevel(self)
		self.player.position = self.beginPosition

		self.difficulity = difficulity

		self.numEnemies = 0

		print("Level " + str(self.difficulity) + "!")

		self.spawnEnemies()
		self.spawnContainers()

	def spawnEnemies(self):
		#If the list at 0 is a list, i.e. we have multiple enemy tags, do for each one.
		#b/c we can have one or multiple enemy tags (which is itself a list),
		#we don't know if the list is going
		#to be singlely or doublely nested.
		print(self.levelData["ENEMY"])
		if (isinstance(self.levelData["ENEMY"][0], list)):
			enemyTagList = self.levelData["ENEMY"]
		else:
			enemyTagList = [self.levelData["ENEMY"]]
		for enemyTag in enemyTagList:
			print(enemyTag)
			enemyFileDir = self.levelFileDirectory + os.sep + enemyTag[0]
			numEnemies = int(enemyTag[1])*self.difficulity
			enemyArchType = enemy.Enemy(enemyFileDir, (0,0))
			for i in range(numEnemies):
				newPos = (random.randrange(0, self.size[0]), random.randrange(0, self.size[1]))
				while (self.checkGround(newPos)):
					newPos = (random.randint(0, self.size[0]), random.randint(0, self.size[1]))
				newEnemy = enemyArchType.clone()
				newEnemy.setPosition(newPos)
				newEnemy.setLevel(self)
				self.addObject(newEnemy)
				self.numEnemies += 1

	def spawnContainers(self):
		#If there are no containers
		if self.levelData.get("PICKUP_CONTAINER", 0) != 0:
			self.spawnTypedContainers(self.levelData["PICKUP_CONTAINER"], pickup.Pickup)

		if self.levelData.get("WEAPON_CONTAINER", 0) != 0:
			self.spawnTypedContainers(self.levelData["WEAPON_CONTAINER"], weapon.Weapon)
		print("Done generating containers!")

	#This function spawns a certain type of container, passed in as the data and the constructor for that type of contents
	def spawnTypedContainers(self, containerData, contentsConstructor):
		#If the list at 0 is a list, i.e. we have multiple container tags, do for each one.
		#b/c we can have one or multiple container tags (which is itself a list),
		#we don't know if the list is going
		#to be singlely or doublely nested.
		if (isinstance(containerData[0], list)):
			containerTagList = containerData
		else:
			containerTagList = [containerData]
		for containerTag in containerTagList:
			print(containerTag)
			containerFileDir = self.levelFileDirectory + os.sep + containerTag[0]
			containerChance = int(containerTag[2])
			if random.randrange(0, containerChance) == 0:
				newPos = (random.randrange(0, self.size[0]), random.randrange(0, self.size[1]))
				while (self.checkGround(newPos)):
					newPos = (random.randint(0, self.size[0]), random.randint(0, self.size[1]))
				newContainer = container.Container(containerFileDir, newPos, self.levelFileDirectory + os.sep + containerTag[1], contentsConstructor)
				self.addObject(newContainer)


	def generatePath(self, position, length, width):
		direction = [0,0]
		direction[random.choice((0,1))] = random.choice([-1,1])

		#for the length of the path
		for i in range(length):
			#get new position
			position = position[0] + direction[0], position[1] + direction[1]

			#make sure not out of bounds in X plus or minus 1 because of edge walls
			if position[0]+width+1 >= self.size[0] or position[0]-width-1 <= 0:
				direction[0] = -direction[0]
				position = position[0] + direction[0], position[1] + direction[1]

			#make sure not out of bounds in Y, plus or minus 1 because of edge walls
			if position[1]+width+1 >= self.size[1] or position[1]-width-1 <= 0:
				direction[1] = - direction[1]
				position = position[0] + direction[0], position[1] + direction[1]

			#Put floor tiles everywhere in the width around our position
			for j in range(-width,width+1):
				for k in range(-width,width+1):	
					self.mapDict[position[0] + j, position[1] + k] = (random.choice(self.floorTiles),0)

					#put walls around the sides of the current area if there are not already tiles there
					for l in range(-1,2):
						for a in range(-1,2):
							possibleWallPos = self.mapDict.get( (position[0] + j+l, position[1] + k+a), (0,0))
							if possibleWallPos[0] == 0:
								self.mapDict[(position[0] + j+l, position[1] + k+a)] = (random.choice(self.wallTiles), 1)

			#If some random chance, choose new direction
			if random.randrange(0,20) == 0:
				direction = [0,0]
				direction[random.choice((0,1))] = random.choice([-1,1])
			#If some random chance, spawn a new path with length = our remaining length
			if random.randrange(0,self.size[0]*self.size[1]) == 0:
				self.generatePath(position, length-i, width)

	def generateMap(self):
		position = (random.randrange(0,self.size[0]), random.randrange(0,self.size[1]))
		#Keep choosing random position until position +- pathWidth is within size.
		while not (position[0] - self.pathWidth > 0 and position[0] + self.pathWidth < self.size[0] and position[1] - self.pathWidth > 0 and position[1] + self.pathWidth < self.size[1]):
			position = ( random.randrange(0,self.size[0]), random.randrange(0,self.size[1]) )
		#Used to set the player's position
		self.beginPosition = position
		self.generatePath(position, self.size[0]*self.size[1]//12, self.pathWidth)

		self.mapSurface = self.drawMap(self.mapDict, self.tileSize, self.size, self.sectionPos, self.wallTiles[0])

	def distribute(self, thingList):
		for i in range(len(thingList)):
			for j in range(i):
				thingList = thingList + [thingList[i]]
		return(thingList)

	def setScreen(self, screen):
		self.screen = screen

	def addObject(self, obj):
		self.objects.append(obj)

	def remove(self, obj):
		self.objectsToRemove.append(obj)

	def checkInBounds(self, obj):
		if obj.position[0] < 0 or obj.position[0] > self.size[0] or obj.position[1] < 0 or obj.position[1] > self.size[1]:
			return(0)
		return(1)

	def checkCollision(self, obj, objRange, excluded):
		collidingList = []
		#Check for objects in list
		for otherObj in self.objects:
			if otherObj != obj and otherObj != excluded and math.fabs(otherObj.position[0] - obj.position[0]) < objRange and math.fabs(otherObj.position[1] - obj.position[1]) < objRange:
				collidingList.append(otherObj)
		#Check for player
		if self.player != obj and self.player != excluded and math.fabs(self.player.position[0] - obj.position[0]) < objRange and math.fabs(self.player.position[1] - obj.position[1]) < objRange:
			collidingList.append(self.player)
		return(collidingList)

	def checkGround(self, position):
		return self.mapDict.get( (math.floor(position[0]), math.floor(position[1]) ), (0,1))[1]

	def update(self, mousePos):
		#Delete all the objects schecueld for removal
		for delObj in self.objectsToRemove:
			if delObj in self.objects:
				self.objects.remove(delObj)
		self.objectsToRemove = []

		for obj in self.objects:
			obj.update(self)
		self.player.update(mousePos)

		self.sectionPos = self.player.position[0] - self.sectionSize[0]//2, self.player.position[1] - self.sectionSize[1]//2

		if self.player.alive == False:
			print("Player Dead!!!")

	def getScreenPosition(self, position):
		return ( self.tileSize[0]*(position[0]-self.sectionPos[0]) + self.sectionPixelOffset[0] + self.recoilOffset[0], self.tileSize[1]*(position[1]-self.sectionPos[1]) + self.sectionPixelOffset[1] + self.recoilOffset[1])

	def addRecoil(self, recoil, recoilAngle):
		self.recoilOffset = int(-recoil*math.cos(recoilAngle)), int(-recoil*math.sin(recoilAngle))

	def draw(self):
		#draw level
		self.screen.blit(self.outOfBoundsSurface, (0,0))
		self.screen.blit(self.mapSurface, (-self.sectionPos[0]*self.tileSize[0]+self.recoilOffset[0],-self.sectionPos[1]*self.tileSize[1]+self.recoilOffset[1]) )
		#draw objects
		for obj in self.objects:
			obj.draw(self)
		self.player.draw(self)
		#Notice the float division, then convert to int. This is because -1//3 is still -1, but int(-1/3) is 0.
		self.recoilOffset = int(self.recoilOffset[0]/2),int(self.recoilOffset[1]/2)

	def drawMap(self, mapDict, tileSize, sectionSize, sectionLocation, defaultTile):
		mapSection = pygame.Surface((tileSize[0]*sectionSize[0], tileSize[1]*sectionSize[1]))
	
		for yPos in range(sectionLocation[1], sectionLocation[1]+sectionSize[1]):
			for xPos in range(sectionLocation[0], sectionLocation[0]+sectionSize[0]):
				mapSection.blit(mapDict.get( (xPos, yPos), (self.outOfBoundsTile,0) )[0], (tileSize[0]*(xPos-sectionLocation[0]), tileSize[1]*(yPos-sectionLocation[1]) ))
		
		return(mapSection)


