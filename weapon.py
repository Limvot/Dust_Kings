import copy
import projectile
from imageAndMapUtil import *

class Weapon:
	def __init__(self, weaponFile, position, owner):

		self.config = loadConfigFile(weaponFile)

		self.owner = owner

		weaponFileDirectory = justDir(weaponFile)
		tileListDir = weaponFileDirectory + os.sep + self.config["TILE"]
		self.tileList = parseImage(tileListDir, (0,0), (int(self.config["TILE_END_X"]),int(self.config["TILE_END_Y"])), 0, -1, 1)
		
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
		newProjectile = copy.copy(self.projectile)
		newProjectile.fire(self.position, self.angle, self.projectileSpeed)
		self.level.addObject(newProjectile)

	def draw(self, level):
		if abs(self.angle) > math.pi/2:
			flipSprite = True
			angle = (self.angle-math.pi)*180/math.pi
		else:
			flipSprite = False
			angle = -self.angle*180/math.pi
		sprite = pygame.transform.rotate(self.tileList[0], angle)
		sprite = pygame.transform.flip(sprite, flipSprite, False)
		level.screen.blit(sprite, level.getScreenPosition(self.position))

