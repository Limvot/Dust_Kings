import math
from imageAndMapUtil import *

class Projectile:
	def __init__(self, projectileFile, owner):

		self.config = loadConfigFile(projectileFile)

		projectileFileDirectory = os.sep.join(projectileFile.split(os.sep)[:-1])
		tileListDir = projectileFileDirectory + os.sep + self.config["TILE"]
		self.tileList = parseImage(tileListDir, (0,0), (int(self.config["TILE_END_X"]),int(self.config["TILE_END_Y"])), 0, -1, 1)

		self.size = int(self.config["SIZE"])
		self.damage = int(self.config["DAMAGE"])

		self.position = (0,0)
		self.velocity = (0,0)

		self.owner = owner

	def fire(self, position, angle, speed):
		self.position = position
		self.velocity = (math.cos(angle)*speed, math.sin(angle)*speed)

	def update(self, level):
		self.position = (self.position[0]+self.velocity[0], self.position[1]+self.velocity[1])
		self.collide(level)

	def collide(self, level):
		if not level.checkInBounds(self):
			level.remove(self)
			return()
		collidee = level.checkCollision(self, self.size, self.owner)
		if collidee != 0:
			collidee.collideWithProjectile(self, level)
			level.remove(self)
			return()
		if level.checkGround(self.position):
			level.remove(self)
			return()

	def collideWithProjectile(self, projectile, level):
		pass
		level.remove(self)

	def draw(self, level):
		level.screen.blit(self.tileList[0], level.getScreenPosition(self.position))


