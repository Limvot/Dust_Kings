import copy
import projectile
import random
from imageAndMapUtil import *

class Weapon:
	def __init__(self, weaponFile, position, owner):

		self.config = loadConfigFile(weaponFile)

		self.owner = owner

<<<<<<< HEAD
		weaponFileDirectory = justDir(weaponFile)
		if (self.config.get("TILE", 0) != 0):
			tileListDir = weaponFileDirectory + os.sep + self.config["TILE"]
			self.tileList = parseImage(tileListDir, (0,0), (int(self.config["TILE_END_X"]),int(self.config["TILE_END_Y"])), 0, -1, 1)
		else:
			self.tileList = 0

		self.numProjectilesToFire = int(self.config.get("NUM_PROJECTILES", 1))

		self.spread = float(self.config.get("SPREAD", 0))
=======
		weaponFileDirectory = justDir(weaponFile)
		tileListDir = weaponFileDirectory + os.sep + self.config["TILE"]
		self.tileList = parseImage(tileListDir, (0,0), (int(self.config["TILE_END_X"]),int(self.config["TILE_END_Y"])), 0, -1, 1)
>>>>>>> e9641c97f8783d24988044ab5c580f85fab6e7a3
		
		self.position = position
		self.angle = 0

		projectilePath = weaponFileDirectory + os.sep + self.config["PROJECTILE"]
		self.projectile = projectile.Projectile(projectilePath, owner)
		self.projectileSpeed = float(self.config["PROJECTILE_SPEED"])

	def clone(self, owner):
		newSelf = copy.copy(self)
		newSelf.projectile = self.projectile.clone()
		#Comment this next line out to create a fun bug.
		#The owner will never not be the enemyArchtype, meaning
		#all enemies when in range of player will shoot themselves
		#and die, making you like Death himself.
		newSelf.setOwner(owner)
		return(newSelf)

	def setOwner(self, owner):
		self.owner = owner
		self.projectile.owner = owner

	def setLevel(self, level):
		self.level = level

	def setPosition(self, position):
		self.position = position

	def setAngle(self, angle):
		self.angle = angle

	def fire(self):
		#Copy our standard projectile and fire it, then add it to the level
		for i in range(self.numProjectilesToFire):
			if self.spread != 0:
				fireAngle = self.angle + (self.spread * random.random() - self.spread/2)
			else:
				fireAngle = self.angle

			newProjectile = copy.copy(self.projectile)
			newProjectile.fire(self.position, fireAngle, self.projectileSpeed)
			self.level.addObject(newProjectile)

	def draw(self, level):

		if abs(self.angle) > math.pi/2:
			flipSprite = True
			angle = (self.angle-math.pi)*180/math.pi
		else:
			flipSprite = False
			angle = -self.angle*180/math.pi

		#if we have a tile
		if self.tileList != 0:
			sprite = pygame.transform.rotate(self.tileList[0], angle)
			sprite = pygame.transform.flip(sprite, flipSprite, False)
			level.screen.blit(sprite, level.getScreenPosition(self.position))

