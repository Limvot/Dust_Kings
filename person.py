#Person.py
import math
from pygame import *
from imageAndMapUtil import *

#This is the person class, which is used by both the player and NPCs. Holds info about the person and has the move and draw functionality
class Person:
	def __init__(self, initTileList, initPos, health, weapons):			#Init with image list (for drawing the charecter) and init to some initial position
		self.position = [0,0]
		self.position[0], self.position[1] = initPos #Assign the position list the values from the initPosition tupel/list
		self.previousPosition = [0,0]
		self.previousPosition[0], self.previousPosition[1] = self.position
		self.tileList = initTileList
		self.weapons = weapons

		self.alive = 1
		self.health = health
		
		self._movingPos = [0,0]			#This variable tells us how far we have to move in each direction. Each time we move a tile, it is advanced toward 0 by 1
		self.ownPixelOffset = [0,0]		#This variable stores the current offset in pixels that we will draw to. It will be multiplied by the number/stage of the subframe drawing to advance
		self._inbetweanMove = False		#Inbetween move is a bool that tells us if we're still moving

		self.faceingDirection = (0,-1)
		self.whichStep = 0

		self.level = 0

	def collideWithProjectile(self, projectile):
		self.health -= projectile.damage
		if self.health <= 0:
			self.alive = 0

	def fireWeapon(self):
		self.weapons[0].fire()

	def cycleWepons(self):
		newFirst = self.weapons.pop()
		self.weapons.insert(0, newFirst)

	def setLevel(self, level):
		self.level = level
		for weapon in self.weapons:
			weapon.setLevel(level)

	def update(self, mousePos):

		self.position = self._movingPos[0]+self.position[0],self._movingPos[1]+self.position[1]
		
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
		self._movingPos[0], self._movingPos[1] = posTup	#Assign our movement variables to the input
		self._inbetweanMove = True

	#This function gets the index into the tile list approite for our direction and self.whichStep
	def getFrameIndex(self):
		if self.faceingDirection == (0,-1):
			if self._inbetweanMove:				#Only use the other move frame's for each self.whichStep if we are moving
				if self.whichStep == 1:
					return(2)
				elif self.whichStep == 2:
					return(0)
				elif self.whichStep == 3:
					return(10)
			return(0)							#Must be self.whichStep 0
		elif self.faceingDirection == (0,1):
			if self._inbetweanMove:				#Only use the other move frame's for each self.whichStep if we are moving
				if self.whichStep == 1:
					return(8)
				elif self.whichStep == 2:
					return(5)
				elif self.whichStep == 3:
					return(11)
			return(5)							#Must be self.whichStep 0
		elif self.faceingDirection == (-1,0):
			if self._inbetweanMove:				#Only use the other move frame's for each self.whichStep if we are moving
				if self.whichStep == 1:
					return(3)
				elif self.whichStep == 2:
					return(6)
				elif self.whichStep == 3:
					return(9)
			return(6)							#Must be self.whichStep 0
		elif self.faceingDirection == (1,0):
			if self._inbetweanMove:				#Only use the other move frame's for each self.whichStep if we are moving
				if self.whichStep == 1:
					return(4)
				elif self.whichStep == 2:
					return(1)
				elif self.whichStep == 3:
					return(7)
			return(1)							#Must be self.whichStep 0

		return(0)

	#This function draws the character.
	def draw(self, level):
		#print(level.getScreenPosition(self.position))
		level.screen.blit(self.tileList[self.getFrameIndex()], level.getScreenPosition(self.position))
		self.weapons[0].draw(level)

