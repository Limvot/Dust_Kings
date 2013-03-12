#monster.py
import random, copy, math
from imageAndMapUtil import *

#This is the monster class

class Monster:
	def __init__(self, initTileList):			#Init with image list (for drawing the monster)
		self.species = 0
		self.item = 0
		self.friendship = 0
		self.nature = "plain"

		self.EVs 		= [0,0,0,0,0,0]
		self.GiveEVs 	= [0,0,0,0,0,0]
		self.IVs 		= [0,0,0,0,0,0]

		generateIVs()


		self.tileList = initTileList
		self.type == "none"
		self.level = 1
		self.experience = 1
		self.baseStats = [0,0,0,0,0,0] #HP, Attack, Defense, SpAttack, SpDefense, Speed
		self.stats = [0,0,0,0,0,0]
		self.battleStats = self.stats.copy()

		self.attacks = [0,0,0,0]

	def __init__(self, baseMonster, level):			#Init with a base level and a monster
		self.tileList = baseMonster.tileList
		self.type == baseMonster.type
		self.level = level
		self.experience = 1
		self.baseStats = baseMonster.baseStats 		#Attack, Defense, SpAttack, SpDefense, Speed
		self.stats = baseMonster.baseStats
		self.battleStats = self.stats

		self.attacks = baseMonster.attacks.copy()

	def generateIVs(self):
		for IV in self.IVs:
			IV = random.randrange(0,32)


	def addExperience(self, otherMonster):
		self.experience += calcExperience(self, otherMonster)
		for EVIndex in range(len(self.EVs)):
			self.EVs[EVIndex] += otherMonster.GiveEVs[EVIndex]

	def setupBattleStats(self):

		#If we haven't calculated health yet... (This function is not called on fainted monsters)
		if self.stats[0] == 0:
			self.stats[0] = calcHealth(self)	#Calculate it

		#Get health from our current health in stats
		self.battleStats[0] = self.stats[0]

		for indexStat in range(1, len(self.stats)):
			self.stats[indexStat] = calcStat(self, indexStat)

	#This function puts changed stats from the battle back into the current stats. (health, poisn, etc)
	def afterBattleStats(self):
		self.stats[0] = self.battleStats[0]

	def updateLevel(self):
		fullyUpdated = False
		while fullyUpdated == False:
			if self.experience >= calcNextLevelExperience(self):
				self.level += 1
			else:
				fullyUpdated = True

	#This function draws the monster.
	def draw(self, surface, position):
		surface.blit(tileList[0], position)


def calcEffectiveness(attack, monster):

	return(1)
	#Should be calculated based on types, ranging 4, 2, 1, .5, .25, 0
	EFFECTIVENESS = 1
	for i in range(len(monster.type)):
			if effective:
				EFFECTIVENESS *= 2
			elif not_effective:
				EFFECTIVENESS *= 0.5
	return(EFFECTIVENESS)

def calcExperience(monster, otherMonster):
	expShare = 1
	luckyEgg = 1
	return( (otherMonster.trained * monster.traded * luckyEgg * otherMonster.level) // (7*expShare) )

def calcHealth(monster):
	return( (((monster.IVs[0] + (2*monster.baseStats[0]) + (monster.EVs[indexStat]/4) + 100) * monster.level)/100) + 10 )

def calcStat(monster, indexStat):
	monster.nature = 1
	return( ((((monster.IVs[indexStat] + (2*monster.baseStats[indexStat]) + (monster.EVs[indexStat]/4) + 100) * monster.level)/100) + 5) * monster.nature )


#Calculates the ammount of experience required to reach the next level
def calcNextLevelExperience(monster):
	level = monster.level + 1

	#Fast
	if monster.growthType == 1:
		return( (4*level**3)//5)

	#Meduium Fast
	elif monster.growthType == 2:
		return(level**3)

	#Medium Slow
	elif monster.growthType == 3:
		return( (6*level**3/5) - 15*level**2 + 100*level - 140)
		
	#Slow
	elif monster.growthType == 4
		return((5*level**3)//4)
	
	#Erratic
	elif monster.growthType == 5:
		if level <= 50:
			return( ( (level**3)*(100-level) )//50 )
		elif level >= 50 and level < 68:
			return( ( (level**3)*(150-level) )//100 )
		elif level >= 68 and level < 98:
			return( ( (level**3)*(math.floor((1911-(10*level))/3)) )//100 )
		elif level >= 98 and level <= 100:
			return( ( (level**3)*(160-level) )//100 )
	#Fluctuating
	elif monster.growthType == 6:
		if level <= 15:
			return( level**3 * ((math.floor((level+1)/3)+24)//50) )
		elif level >= 15 and level < 36:
			return( level**3 * ((level+14)//50) )
		elif level >= 36 and level <= 100:
			return( level**3 * ((math.floor(level/2)+32)//50) )
	#If none of these, which would be wierd, return a generic growth
	return(level**3)



#This function calculates the attack between this monster and some other givin an attack
def calcAttack(ourMonster, attack, otherMonster):

	#Bonus given if attack type and monster type is same
	STAB = 1
	for i in range(len(ourMonster.type)):
		if ourMonster.type[i] == attack.type:
			STAB *= 1.5

	EFFECTIVENESS = calcEffectiveness(attack, otherMonster)

	#							AttackType indexes into attack or special attack 						Same for defenseType
	if criticalHit: #Critical hit doubles level and uses non affected stats
		damage = ((((((4*ourMonster.level/5+2)*ourMonster.stats[attackType]*attack.attack)/otherMonster.stats[defenseType])/50)+2)*STAB*EFFECTIVENESS)/(random.randint(217,255)/255)
	else:
		damage = ((((((2*ourMonster.level/5+2)*ourMonster.battleStats[attackType]*attack.attack)/otherMonster.battleStats[defenseType])/50)+2)*STAB*EFFECTIVENESS)/(random.randint(217,255)/255)
	return(damage)




