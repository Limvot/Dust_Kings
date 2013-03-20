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

gameConfig = loadConfigFile("game.txt")
GAME_NAME = " ".join(gameConfig["GAME_NAME"])
pygame.display.set_caption(GAME_NAME)

screen = pygame.display.set_mode( screenSize )
background = pygame.Surface(screen.get_size())
background.fill( (100,100,100) )
background.blit(load_image(gameConfig["TITLE_SCREEN"])[0], (0,0))
screen.blit(background, (0,0))
pygame.display.flip()

getKey(-1)

#Wait for input
background.blit(load_image(gameConfig["MENU_BACKGROUND"])[0], (0,0))


def goMenu():
	screen.blit(background, (0,0))		#Draw our background

	if pygame.font:					#Only if fonts are enabled
		textOffset = screen.get_size()[1]//(len(gameConfig["CHARACTERS"])+2)
		font = pygame.font.Font(None, 48)										#Font size
		text = font.render(GAME_NAME, 1, (10, 10, 10))							#Font message
		textpos = text.get_rect(centerx=screen.get_width()//2)					#Center of screen
		screen.blit(text, textpos)												#Draw

		font = pygame.font.Font(None, 28)										#Font size
		text = font.render("Choose a character", 1, (10, 10, 10))
		textpos = text.get_rect(centerx=screen.get_width()//3)
		
		screen.blit(text, (textpos[0], textpos[1]+textOffset))
		
		font = pygame.font.Font(None, 24)
		for i in range(len(gameConfig["CHARACTERS"])):
			charOption = "("+str(i)+") " + gameConfig["CHARACTERS"][i].split("/")[-1].split(".")[0] #Use the name of the file minus the extension and the path
			text = font.render(charOption, 1, (10, 10, 10))
			textpos = text.get_rect(centerx=screen.get_width()//2)
			screen.blit(text, (textpos[0], textOffset*(i+2)))


	pygame.display.flip()			#Flip our display


	goOverworld(gameConfig["CHARACTERS"][int(getKey(-1))])

def goMessageScreen(message, keyWait):
	screen.blit(background, (0,0))		#Draw our background

	if pygame.font:					#Only if fonts are enabled										#Draw
		font = pygame.font.Font(None, 38)										#Font size
		text = font.render(message, 1, (10, 10, 10))
		textpos = text.get_rect(centerx=screen.get_width()//2)
		
		screen.blit(text, (textpos[0], textpos[1]))

	pygame.display.flip()			#Flip our display
	getKey(keyWait)
			


def goOverworld(player):
	global screen
	fullscreen = False

	#playerTileList = parseImage("data/sprMutant1Walk_strip4.png", (0,0), (24,24), 0, -1, 1)
	#weaponTileList = parseImage("data/sprBanditGun.png", (0,0), (24,8), 0, -1, 1)
	#projectileTileList = parseImage("data/sprBullet1_strip2.png", (0,0), (16,16), 0, -1, 1)
	#level = Level("data/level1.txt", screen, Person(playerTileList, (0,0), 3, [Weapon(weaponTileList,(0,0),Projectile(projectileTileList,1,2),1.5)]))
	difficulty = 1
	level = Level(gameConfig["LEVEL_ROTATION"][0], screen, Person(player, (0,0)), difficulty)
	multiplier = 1


	mousePos = (0,0)
	movingPos = (0,0)

	currentLevel = 0
	achievedWin = False

	stop = False
	while stop == False:		#Go until we quit

		level.update(mousePos)
		level.draw()

		stop = not level.player.alive

		if level.numEnemies == 0:
			difficulty += 1
			if difficulty % int(gameConfig["LEVEL_ROTATE_EVERY"]) == 0:
				currentLevel += 1
				if currentLevel >= len(gameConfig["LEVEL_ROTATION"]):
					currentLevel = 0
			if difficulty == 10:
				goMessageScreen(" ".join(gameConfig["WIN_MESSAGE"]), -1)
				achievedWin = True
			level = Level(gameConfig["LEVEL_ROTATION"][currentLevel], screen, Person(player, (0,0)), difficulty)

		level.player.go( movingPos )

		stop = not level.player.alive

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

	if achievedWin:
		goMessageScreen(" ".join(gameConfig["WIN_DEATH_MESSAGE"]), -1)
	else:
		goMessageScreen(" ".join(gameConfig["DEATH_MESSAGE"]), -1)

goMenu() #Run our menu to start
