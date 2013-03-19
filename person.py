#Person.py
import math
import copy
import weapon
from pygame import *
from imageAndMapUtil import *

#This is the person class, which is used by both the player and NPCs. Holds info about the person and has the move and draw functionality
class Person:
	def __init__(self, characterFile, initPos):			#init to some initial position
		self.position = initPos #Assign the position list the values from the initPosition tupel/list
		self.previousPosition = [0,0]
		self.previousPosition[0], self.previousPosition[1] = self.position

		self.config = loadConfigFile(characterFile)

		self.tileEnd = (int(self.config["TILE_END_X"]),int(self.config["TILE_END_Y"]))
		self.tileOffset = (int(self.config["TILE_OFFSET_X"]),int(self.config["TILE_OFFSET_Y"]))

		characterFileDirectory = justDir(characterFile)

		idleTileDir = characterFileDirectory + os.sep + self.config["IDLE"]
		self.idleTiles = parseImage(idleTileDir, (0,0), self.tileEnd, 0, -1, 1)

		walkTileDir = characterFileDirectory + os.sep + self.config["WALK"]
		self.walkTiles = parseImage(walkTileDir, (0,0), self.tileEnd, 0, -1, 1)
		
		defaultWeaponPath = characterFileDirectory + os.sep + self.config["DEFAULT_WEAPON"]
		self.weapons = [weapon.Weapon(defaultWeaponPath, self.position, self)]

		self.framesPerSprite = int(self.config["FRAMES_PER_SPRITE"])

		self.alive = True
		self.health = int(self.config["HEALTH"])

		self.speed = float(self.config["SPEED"])
		
		self._movingPos = [0,0]			#This variable tells us how far we have to move in each direction. Each time we move a tile, it is advanced toward 0 by 1
		self.ownPixelOffset = [0,0]		#This variable stores the current offset in pixels that we will draw to. It will be multiplied by the number/stage of the subframe drawing to advance
		self._inbetweanMove = False		#Inbetween move is a bool that tells us if we're still moving

		self.faceingDirection = (0,-1)
		self.whichStep = 0

		self.level = 0

	def clone(self):
		newSelf = copy.copy(self)
		newWeapons = []
		for weapon in self.weapons:
			newWeapons.append(weapon.clone(newSelf))
		newSelf.weapons = newWeapons
		return(newSelf)


	def collideWithProjectile(self, projectile, level):
		self.health -= projectile.damage
		print(self, "Hit by projectile", projectile, "with owner", projectile.owner)
		print(self.health)
		if self.health <= 0:
			self.alive = False
			self.die()

	def die(self):
		print("Person Died!")

	def fireWeapon(self):
		self.weapons[0].fire()

	def cycleWepons(self):
		newFirst = self.weapons.pop()
		self.weapons.insert(0, newFirst)

	def setLevel(self, level):
		self.level = level
		for weapon in self.weapons:
			weapon.setLevel(level)

	def setPosition(self, position):
		self.position = position

	def update(self, mousePos):
		newPos = self._movingPos[0]+self.position[0],self._movingPos[1]+self.position[1]
		if not self.level.checkGround(newPos):
			self.position = newPos
		else:
			newPos = self._movingPos[0]+self.position[0],self.position[1]
			if not self.level.checkGround(newPos):
				self.position = newPos
			else:
				newPos = self.position[0],self._movingPos[1]+self.position[1]
				if not self.level.checkGround(newPos):
					self.position = newPos
		
		relY = mousePos[1] - self.level.getScreenPosition(self.position)[1]
		relX = mousePos[0] - self.level.getScreenPosition(self.position)[0]
		#don't devide by zero
		if relX == 0:
			relX = 1

		mouseAngle = math.atan(relY/relX)
		if relY <= 0 and relX <= 0:
			mouseAngle -= math.pi
		elif relY > 0 and relX <=0:
			mouseAngle += math.pi
		for weapon in self.weapons:
			weapon.setAngle(mouseAngle)
			weapon.setPosition(self.position)

	#This function tells the character how far to move, starting the move
	def go(self, posTup):
		self._movingPos[0], self._movingPos[1] = posTup[0]*self.speed, posTup[1]*self.speed	#Assign our movement variables to the input
		self._inbetweanMove = True

	#This function gets the index into the tile list approite for our direction and self.whichStep
	def getCurrentSprite(self):
		if self._movingPos[0] != 0 or self._movingPos[1] != 0 :
			tileList = self.walkTiles
		else:
			tileList = self.idleTiles

		self.whichStep += 1
		if self.whichStep >= len(tileList)*self.framesPerSprite:
			self.whichStep = 0

		if abs(self.weapons[0].angle) > math.pi/2:
			flipSprite = True
		else:
			flipSprite = False

		return(pygame.transform.flip(tileList[self.whichStep//self.framesPerSprite], flipSprite, False))

	#This function draws the character.
	def draw(self, level):
		#print(level.getScreenPosition(self.position))
		screenPosition = level.getScreenPosition(self.position)
		drawPosition =  screenPosition[0] + self.tileOffset[0], screenPosition[1] + self.tileOffset[1] #Probally negative
		level.screen.blit(self.getCurrentSprite(), drawPosition)
		self.weapons[0].draw(level)

