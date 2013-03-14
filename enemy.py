#Person.py
import math
import weapon
import person
import random
from pygame import *
from imageAndMapUtil import *

#This is the person class, wwhich is used by both the player and NPCs. Holds info about the person and has the move and draw functionality
class Enemy(person.Person):
	def __init__(self, characterFile, initPos):
		super(Enemy, self).__init__(characterFile, initPos)
		self.range = int(self.config["SIGHT_RANGE"])
		self.fireChance = int(self.config["FIRE_CHANCE"])

	def clone(self):
		newSelf = super(Enemy, self).clone()
		newSelf.range = self.range
		newSelf.fireChance = self.fireChance
		return(newSelf)

	def die(self):
		print("Enemy dead!")
		self.level.numEnemies -= 1
		print("Number of enemies:",self.level.numEnemies)
		self.level.remove(self)

	def update(self, mousePos):
		newPos = self._movingPos[0]+self.position[0],self._movingPos[1]+self.position[1]
		if not self.level.checkGround(newPos):
			self.position = newPos
		
		relY = self.level.player.position[1] - self.position[1]
		relX = self.level.player.position[0] - self.position[0]

		#don't devide by zero
		if relX == 0:
			relX = 1

		aimAngle = math.atan(relY/relX)
		if relY <= 0 and relX <= 0:
			aimAngle -= math.pi
		elif relY > 0 and relX <=0:
			aimAngle += math.pi
		for weapon in self.weapons:
			weapon.setAngle(aimAngle)
			weapon.setPosition(self.position)

		self.go( (0,0) )
		if random.randrange(0,int(self.config["FOLLOW_CHANCE"])) == 0:
			self.go((math.cos(aimAngle), math.sin(aimAngle)))

		if abs(self.level.player.position[0] - self.position[0]) < self.range and abs(self.level.player.position[1] - self.position[1]) < self.range:
			if random.randrange(0, self.fireChance) == 0:
				self.fireWeapon()