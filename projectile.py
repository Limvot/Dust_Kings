import math
import copy
from imageAndMapUtil import *

class Projectile:
	def __init__(self, projectileFile, owner):

		self.config = loadConfigFile(projectileFile)

		projectileFileDirectory = justDir(projectileFile)
		tileListDir = projectileFileDirectory + os.sep + self.config["TILE"]
		self.tileList = parseImage(tileListDir, (0,0), (int(self.config["TILE_END_X"]),int(self.config["TILE_END_Y"])), 0, -1, 1)

		self.size = int(self.config["SIZE"])
		self.damage = int(self.config["DAMAGE"])

		self.position = (0,0)
		self.velocity = (0,0)
		self.angle = 0
		self.framesLived = 0

		self.owner = owner

	def clone(self):
		return(copy.copy(self))

	def fire(self, position, angle, speed):
		self.firstFrame = True
		self.position = position
		self.angle = angle
		self.velocity = (math.cos(angle)*speed, math.sin(angle)*speed)

	def update(self, level):
		self.framesLived +=1
		self.position = (self.position[0]+self.velocity[0], self.position[1]+self.velocity[1])
		self.collide(level)

	def collide(self, level):
		if not level.checkInBounds(self):
			level.remove(self)
			return()
		collidee = level.checkCollision(self, self.size, self.owner)
		if collidee != 0:
			collidee.collideWithProjectile(self, level)
			if isinstance(collidee, Projectile):
				if self.collideWithProjectile(collidee, level):
					return()
			else:
				level.remove(self)
				return()
		if level.checkGround(self.position):
			level.remove(self)

	def collideWithProjectile(self, projectile, level):
		if projectile.owner != self.owner:
			level.remove(self)
			return(True)
		return(False)

	def draw(self, level):
		if self.framesLived < 2 or len(self.tileList) == 1:
			index = 0
		else:
			index = 1
		if abs(self.angle) > math.pi/2:
			flipSprite = True
			angle = (self.angle-math.pi)*180/math.pi
		else:
			flipSprite = False
			angle = -self.angle*180/math.pi
		sprite = pygame.transform.rotate(self.tileList[index], angle)
		sprite = pygame.transform.flip(sprite, flipSprite, False)
		level.screen.blit(sprite, level.getScreenPosition(self.position))


