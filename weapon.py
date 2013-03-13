import copy
import projectile
from imageAndMapUtil import *

class Weapon:
	def __init__(self, weaponFile, position, owner):

		self.config = loadConfigFile(weaponFile)

		weaponFileDirectory = os.sep.join(weaponFile.split(os.sep)[:-1])
		tileListDir = weaponFileDirectory + os.sep + self.config["TILE"]
		self.tileList = parseImage(tileListDir, (0,0), (int(self.config["TILE_END_X"]),int(self.config["TILE_END_Y"])), 0, -1, 1)
		
		self.position = position
		self.angle = 0

		projectilePath = weaponFileDirectory + os.sep + self.config["PROJECTILE"]
		self.projectile = projectile.Projectile(projectilePath, owner)
		self.projectileSpeed = float(self.config["PROJECTILE_SPEED"])

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

