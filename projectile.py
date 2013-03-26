import math
import copy
import person
import os
from imageAndMapUtil import *

class Projectile:
	def __init__(self, projectileFile, position, owner):

		self.config = loadConfigFile(projectileFile)

		projectileFileDirectory = justDir(projectileFile)
		tileListDir = projectileFileDirectory + os.sep + self.config["TILE"]
		self.tileList = parseImage(tileListDir, (0,0), (int(self.config["TILE_END_X"]),int(self.config["TILE_END_Y"])), 0, -1, 1)

		self.size = int(self.config["SIZE"])
		self.damage = int(self.config["DAMAGE"])

		self.lifetime = int(self.config.get("LIFETIME", 0))

		self.position = position
		self.velocity = (0,0)
		self.knockback = 0
		self.angle = 0
		self.framesLived = 0

		#If we create another projectile when we die, set it up
		self.onDeath = self.config.get("ON_DEATH", 0)
		if self.onDeath != 0:
			self.onDeath = Projectile(projectileFileDirectory + os.sep + self.onDeath, self.position, owner)

		self.owner = owner

	def clone(self):
		return(copy.copy(self))

	def fire(self, position, angle, speed, knockback):
		newProjectile = self.clone()
		newProjectile.framesLived = 0
		newProjectile.position = position
		newProjectile.angle = angle
		newProjectile.knockback = knockback
		newProjectile.speed = speed
		newProjectile.velocity = (math.cos(angle)*speed, math.sin(angle)*speed)
		return(newProjectile)

	def die(self, level):
		if self.onDeath != 0:
			self.onDeath.fire(self.position, self.angle, self.speed, self.knockback)
			level.addObject(self.onDeath.fire(self.position, self.angle, self.speed, self.knockback))
		level.remove(self)

	def update(self, level):
		self.framesLived +=1
		self.position = (self.position[0]+self.velocity[0], self.position[1]+self.velocity[1])
		self.collide(level)

		if self.lifetime != 0 and self.lifetime < self.framesLived:
			self.die(level)

	def collide(self, level):
		if not level.checkInBounds(self):
			self.die(level)
			return()
		for collidee in level.checkCollision(self, self.size, self.owner):
			collidee.collideWithProjectile(self, level)
			if isinstance(collidee, Projectile):
				self.collideWithProjectile(collidee, level)
			#Only collide with alive entities, dead ones don't matter.
			elif isinstance(collidee, person.Person):
				if collidee.alive:
					self.die(level)
					return()

		if level.checkGround(self.position):
			self.die(level)

	def collideWithProjectile(self, projectile, level):
		if projectile.owner != self.owner:
			self.die(level)
			return(True)
		return(False)

	def draw(self, level):
		if self.framesLived > len(self.tileList):
			index = len(self.tileList)-1
		else:
			index = self.framesLived-1

		if abs(self.angle) > math.pi/2:
			flipSprite = True
			angle = (self.angle-math.pi)*180/math.pi
		else:
			flipSprite = False
			angle = -self.angle*180/math.pi
		sprite = pygame.transform.rotate(self.tileList[index], angle)
		sprite = pygame.transform.flip(sprite, flipSprite, False)
		#Draw so that position is center of object
		levelPos = level.getScreenPosition(self.position)
		drawPos = levelPos[0]-sprite.get_width()//2,levelPos[1]-sprite.get_height()//2
		level.screen.blit(sprite, drawPos)


