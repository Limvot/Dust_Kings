import copy
from imageAndMapUtil import *

class Weapon:
	def __init__(self, tileList, position, projectile, projectileSpeed):
		self.tileList = tileList
		self.position = position
		self.angle = 0
		self.projectile = projectile
		self.projectileSpeed = projectileSpeed

	def setLevel(self, level):
		self.level = level

	def setPosition(self, position):
		self.position = position

	def setAngle(self, angle):
		self.angle = angle

	def fire(self):
		#Copy our standard projectile and fire it, then add it to the level
		newProjectile = copy.copy(self.projectile)
		newProjectile.fire(self.position, self.angle, self.projectileSpeed)
		self.level.addObject(newProjectile)

	def draw(self, level):
		level.screen.blit(self.tileList[0], level.getScreenPosition(self.position))

