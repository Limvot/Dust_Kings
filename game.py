from imageAndMapUtil import *
from person import *
from weapon import *
from projectile import *
from level import *

#init the pygame stuff
pygame.init()

clock = pygame.time.Clock()

mousePos = (0,0)


loadTileSize = (16,16)
tileSize = (loadTileSize[0]*2,loadTileSize[1]*2)	#Maps are stored at half res, have to be scaled up

frameDelay = 20

#We have a big screen
screenSizeMultipler = 1
screenSize = (420*screenSizeMultipler,340*screenSizeMultipler)
sectionSize = ( (screenSize[0]//tileSize[0]+1), (screenSize[1]//tileSize[1]+1) )	#Adjust the tile section size to the screen size, so that it covers the entire screen
screen = pygame.display.set_mode( screenSize )
gray = pygame.Surface(screenSize)													#This grey is our background which shouldn't really ever show through
gray.fill( (185,200,254) )
gameConfig = loadConfigFile("data/game.txt")
GAME_NAME = " ".join(gameConfig["GAME_NAME"])
pygame.display.set_caption(GAME_NAME)


def goMenu():
	screen.blit(gray, (0,0))		#Draw our gray background
	if pygame.font:					#Only if fonts are enabled
		font = pygame.font.Font(None, 68)										#Font size
		text = font.render(GAME_NAME, 1, (10, 10, 10))		#Font message
		textpos = text.get_rect(centerx=screen.get_width()//2)					#Center of screen
		screen.blit(text, textpos)												#Draw

		font = pygame.font.Font(None, 48)										#Font size

		text = font.render("Play!", 1, (10, 10, 10))					#Each of these are the same, but drawn to the first 1/3 of the screen
		textpos = text.get_rect(centerx=screen.get_width()//3)
		
		screen.blit(text, (textpos[0], textpos[1]+100))

		text = font.render("or (Q)uit!", 1, (10, 10, 10))
		textpos = text.get_rect(centerx=screen.get_width()//3)
		screen.blit(text, (textpos[0], textpos[1]+400))


	pygame.display.flip()			#Flip our display

	goOverworld("h")
			


def goOverworld(world):
	global screen
	fullscreen = False

	#playerTileList = parseImage("data/sprMutant1Walk_strip4.png", (0,0), (24,24), 0, -1, 1)
	#weaponTileList = parseImage("data/sprBanditGun.png", (0,0), (24,8), 0, -1, 1)
	#projectileTileList = parseImage("data/sprBullet1_strip2.png", (0,0), (16,16), 0, -1, 1)
	#level = Level("data/level1.txt", screen, Person(playerTileList, (0,0), 3, [Weapon(weaponTileList,(0,0),Projectile(projectileTileList,1,2),1.5)]))
	difficulty = 1
	level = Level("data/level1.txt", screen, Person("data/playerEyes.txt", (0,0)), difficulty)
	multiplier = 1


	mousePos = (0,0)

	movingPos = (0,0)

	stop = False
	while stop == False:		#Go until we quit

		level.update(mousePos)
		level.draw()

		stop = not level.player.alive

		if level.numEnemies == 0:
			difficulty += 1
			level = Level("data/level1.txt", screen, Person("data/playerEyes.txt", (0,0)), difficulty)

		level.player.go( movingPos )

		for event in pygame.event.get():
			if event.type == KEYDOWN:
				userInput = pygame.key.name(event.key)
				if userInput == "left" or userInput == "a":
					movingPos = movingPos[0] - 1, movingPos[1]
				elif userInput == "right" or userInput == "d":
					movingPos = movingPos[0] + 1, movingPos[1] 
				elif userInput == "up" or userInput == "w":
					movingPos = movingPos[0], movingPos[1] - 1
				elif userInput == "down" or userInput == "s":
					movingPos = movingPos[0], movingPos[1] + 1
				elif userInput == "x":
					multiplier -= 1
				elif userInput == "z":
					multiplier += 1
				elif userInput == "x":
					multiplier -= 1
				elif userInput == "1":
					level = Level("data/level1.txt", screen, Person("data/playerEyes.txt", (0,0)), difficulty)
				elif userInput == "2":
					level = Level("data/level2.txt", screen, Person("data/playerEyes.txt", (0,0)), difficulty)
				elif userInput == "3":
					level = Level("data/level3.txt", screen, Person("data/playerEyes.txt", (0,0)), difficulty)
				elif userInput == "f":
					fullscreen = False if fullscreen else True
					if fullscreen:
						screen = pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
					else:
						screen = pygame.display.set_mode(screenSize)
					level.setScreen(screen)
				elif userInput == "escape":
					stop = True

			elif event.type == KEYUP:
				userInput = pygame.key.name(event.key)
				if userInput == "left" or userInput == "a":
					movingPos = movingPos[0] + 1, movingPos[1]
				elif userInput == "right" or userInput == "d":
					movingPos = movingPos[0] - 1, movingPos[1]
				elif userInput == "up" or userInput == "w":
					movingPos = movingPos[0], movingPos[1] + 1
				elif userInput == "down" or userInput == "s":
					movingPos = movingPos[0], movingPos[1] - 1

			elif event.type == MOUSEMOTION:
				mousePos = event.pos
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					level.player.fireWeapon()
				elif event.button == 2:
					print("What do you want middle click to do anyway?")
				elif event.button == 3:
					print("No special yet....")
			elif event.type == QUIT:
				stop = True

		pygame.time.wait(15)
	print("You did not become either the Wasteland King or the Dust King!")

goMenu() #Run our menu to start