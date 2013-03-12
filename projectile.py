import math

class Projectile:
	def __init__(self, tileList, size, damage):
		self.tileList = tileList
		self.size = size
		self.damage = damage

		self.position = (0,0)
		self.velocity = (0,0)

	def fire(self, position, angle, speed):
		self.position = position
		self.velocity = (math.cos(angle)*speed, math.sin(angle)*speed)

	def update(self):
		self.position = (self.position[0]+self.velocity[0], self.position[1]+self.velocity[1])

	def collide(self, level):
		if not level.checkInBounds(self):
			level.remove(self)
		collidee = level.checkCollision(self.position, self.size)
		if collidee != 0:
			collidee.collideWithProjectile(self)

	def draw(self, level):
		level.screen.blit(self.tileList[0], level.getScreenPosition(self.position))


