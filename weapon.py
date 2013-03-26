import copy
import projectile
import random
import person
from imageAndMapUtil import *

#Weapons are both used when held by persons and just sitting in the level, waiting to be picked up.
#Since weapons to be constructed with owners, the owner when just in the level is the level by convention.
class Weapon:
	def __init__(self, weaponFile, position, owner):

		self.config = loadConfigFile(weaponFile)

		self.owner = owner

		weaponFileDirectory = justDir(weaponFile)
		if (self.config.get("TILE", 0) != 0):
			tileListDir = weaponFileDirectory + os.sep + self.config["TILE"]
			self.tileList = parseImage(tileListDir, (0,0), (int(self.config["TILE_END_X"]),int(self.config["TILE_END_Y"])), 0, -1, 1)
		else:
			self.tileList = 0

		self.numProjectilesToFire = int(self.config.get("NUM_PROJECTILES", 1))

		self.spread = float(self.config.get("SPREAD", 0))
		weaponFileDirectory = justDir(weaponFile)
	
		self.position = position
		self.angle = 0

		projectilePath = weaponFileDirectory + os.sep + self.config["PROJECTILE"]
		self.projectile = projectile.Projectile(projectilePath, self.position, owner)
		self.projectileSpeed = float(self.config["PROJECTILE_SPEED"])

		self.ammoType = projectilePath.split("/")[-1]

		if isinstance(self.owner, person.Person):
			self.owner.addAmmo(self.ammoType, int(self.config.get("AMMO_NUM", -1)))

		self.recoil = int(self.config.get("RECOIL", 0))
		self.knockback = int(self.config.get("KNOCKBACK", 0))

		self.sight = self.config.get("LASER_SIGHT", 0 )
		if self.sight != 0:
			self.sight = int(self.sight[0]), int(self.sight[1]), int(self.sight[2])

	def clone(self, owner):
		newSelf = copy.copy(self)
		newSelf.projectile = self.projectile.clone()
		#Comment this next line out to create a fun bug.
		#The owner will always be the enemyArchtype, meaning
		#all enemies when in range of player will shoot themselves
		#and die, making you like Death himself.
		newSelf.setOwner(owner)
		return(newSelf)

	def setOwner(self, owner):
		self.owner = owner
		self.projectile.owner = owner
		if isinstance(self.owner, person.Person):
			self.owner.addAmmo(self.ammoType, int(self.config.get("AMMO_NUM", -1)))

	def setLevel(self, level):
		self.level = level

	def setPosition(self, position):
		self.position = position

	def setAngle(self, angle):
		self.angle = angle

	def fire(self):
		#If our owner has enough ammo, copy our standard projectile and fire it, then add it to the level
		if self.owner.useAmmo(self.ammoType, self.numProjectilesToFire):
			for i in range(self.numProjectilesToFire):
				if self.spread != 0:
					fireAngle = self.angle + (self.spread * random.random() - self.spread/2)
				else:
					fireAngle = self.angle

				self.level.addObject(self.projectile.fire(self.position, fireAngle, self.projectileSpeed, self.knockback))

			self.level.addRecoil(self.recoil, self.angle)

	#This function is used when the weapon is in the level, but not picked up. Just sitting there.
	def update(self, mousePos):
		pass
		
	#projectiles don't matter
	def collideWithProjectile(self, projectile, level):
		return(False)

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
			
			#Draw so that position is center of object
			levelPos = level.getScreenPosition(self.position)
			drawPos = levelPos[0]-sprite.get_width()//2,levelPos[1]-sprite.get_height()//2
			level.screen.blit(sprite, drawPos)
		if self.sight != 0:
			drawLength = level.size[0]*level.tileSize[0]+level.size[1]*level.tileSize[1]
			#Start Drawing at end of barrel, which is about half as long as the tile
			drawPosBegin = int(levelPos[0]+math.cos(self.angle)* self.tileList[0].get_width()//2), int(levelPos[1]+math.sin(self.angle)*self.tileList[0].get_height()//2)
			#Stop drawing somewhere far beyond screen, (about as long as the level)
			drawPosEnd = int(levelPos[0]+math.cos(self.angle)*drawLength), int(levelPos[1]+math.sin(self.angle)*drawLength)
			pygame.draw.line(level.screen, self.sight, drawPosBegin, drawPosEnd)

