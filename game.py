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

gameConfig = loadConfigFile("game.txt")

screenSizeTag = gameConfig.get("SCREEN_SIZE", (320,240))
screenSize = int(screenSizeTag[0]), int(screenSizeTag[1])
screenSizeMultiplier = int(gameConfig.get("DRAW_MULTIPLIER", 2))
trueScreenSize = screenSize[0]*screenSizeMultiplier, screenSize[1]*screenSizeMultiplier
sectionSize = ( (screenSize[0]//tileSize[0]+1), (screenSize[1]//tileSize[1]+1) )	#Adjust the tile section size to the screen size, so that it covers the entire screen

GAME_NAME = " ".join(gameConfig["GAME_NAME"])
pygame.display.set_caption(GAME_NAME)

FONT_FILE = gameConfig["FONT"]
FONT_SIZE = int(gameConfig["FONT_SIZE"])
FONT_TITLE_SIZE = int(gameConfig["FONT_TITLE_SIZE"])
FONT_HUD_SIZE = int(gameConfig["FONT_HUD_SIZE"])

windowScreen = pygame.display.set_mode( (screenSize[0]*screenSizeMultiplier,screenSize[1]*screenSizeMultiplier) )
screen = pygame.Surface( screenSize )
background = pygame.Surface(screen.get_size())
background.fill( (100,100,100) )

drawCustomMouse = False
if gameConfig.get("MOUSE", 0) != 0:
	pygame.mouse.set_visible(False)
	mouseCursor = load_image(gameConfig["MOUSE"])[0]
	drawCustomMouse = True


def drawToWindow(screen):
	windowScreen.blit(pygame.transform.scale(screen, (screenSize[0]*screenSizeMultiplier,screenSize[1]*screenSizeMultiplier) ), (0,0))
	pygame.display.flip()

def goTitleScreen():
	background.blit(load_image(gameConfig["TITLE_SCREEN"])[0], (0,0))
	screen.blit(background, (0,0))
	drawToWindow(screen)
	getKey(-1)
	goMenu()

def goMenu():
	background.blit(load_image(gameConfig["MENU_BACKGROUND"])[0], (0,0))
	screen.blit(background, (0,0))		#Draw our background

	if pygame.font:					#Only if fonts are enabled
		textOffset = screen.get_size()[1]//(len(gameConfig["CHARACTERS"])+2)
		font = pygame.font.Font(FONT_FILE, FONT_TITLE_SIZE)										#Font size
		text = font.render(GAME_NAME, 1, (10, 10, 10))							#Font message
		textpos = text.get_rect(centerx=screen.get_width()//2)					#Center of screen
		screen.blit(text, textpos)												#Draw

		font = pygame.font.Font(FONT_FILE, FONT_SIZE)										#Font size
		text = font.render("Choose a character", 1, (10, 10, 10))
		textpos = text.get_rect(centerx=screen.get_width()//3)
		
		screen.blit(text, (textpos[0], textpos[1]+textOffset))
		
		font = pygame.font.Font(FONT_FILE, FONT_SIZE)
		for i in range(len(gameConfig["CHARACTERS"])):
			charOption = "("+str(i)+") " + gameConfig["CHARACTERS"][i].split("/")[-1].split(".")[0] #Use the name of the file minus the extension and the path
			text = font.render(charOption, 1, (10, 10, 10))
			textpos = text.get_rect(centerx=screen.get_width()//2)
			screen.blit(text, (textpos[0], textOffset*(i+2)))


	drawToWindow(screen)


	goOverworld(gameConfig["CHARACTERS"][int(getKey(-1))])

def goMessageScreen(messages, keyWait):
	screen.blit(background, (0,0))		#Draw our background

	offset = 0

	#Allow both lists and single strings
	if not isinstance(messages, list):
		messages = [messages] 

	if pygame.font:					#Only if fonts are enabled
		font = pygame.font.Font(FONT_FILE, FONT_SIZE)
		for message in messages:
			text = font.render(message, 1, (10, 10, 10))
			textpos = text.get_rect(centerx=screen.get_width()//2, centery=screen.get_height()//3 + offset)
			offset += text.get_height()
			screen.blit(text, (textpos[0], textpos[1]))

	drawToWindow(screen)
	getKey(keyWait)

def drawHUD(level, expBar, healthBar):
	BUFFER = 10

	healthStr = str(level.player.health) + "/" + str(level.player.maxHealth)
	exp = level.player.exp - level.player.expPerLevel*level.player.plrLevel 

	expBarSize = expBar[0].get_size()
	healthBarSize = healthBar[0].get_size()

	if pygame.font:					#Only if fonts are enabled										#Draw
		font = pygame.font.Font(FONT_FILE, FONT_HUD_SIZE)

		#Experience
		expPct = int(exp/level.player.expPerLevel * (len(expBar)-1))
		screen.blit(expBar[expPct], (0,0) )
		text = font.render(str(exp), 1, (10, 10, 10))
		expBlitPos = expBarSize[0]//2 - text.get_width()//2, expBarSize[1] + BUFFER
		screen.blit(text, expBlitPos)

		#Health
		healthPct = (len(healthBar)-1)-int(level.player.health/level.player.maxHealth * (len(healthBar)-1))
		screen.blit(healthBar[healthPct], (expBarSize[0]+BUFFER,0) )
		text = font.render(healthStr, 1, (10, 10, 10))
		healthBlitPos = healthBarSize[0]//2 - text.get_width()//2, healthBarSize[1]//2 - text.get_height()//2
		healthBlitPos = healthBlitPos[0]+expBarSize[0]+BUFFER, healthBlitPos[1]
		screen.blit(text, healthBlitPos )

		#Ammo
		ammoBlitPos = healthBlitPos[0] + BUFFER, healthBlitPos[1] + BUFFER
		for ammoType in level.player.ammo.items():
			text = font.render(ammoType[0] + "-"+str(ammoType[1]), 1, (10, 10, 10))
			ammoBlitPos = ammoBlitPos[0], ammoBlitPos[1] + text.get_height()
			screen.blit(text, ammoBlitPos )

	else:
		print(expStr, HUDString)

	#Weapons
	weaponDrawOffset = 0
	for playerWeapon in level.player.weapons:
		if playerWeapon.tileList != 0:
			screen.blit(playerWeapon.tileList[0], (expBarSize[0]+BUFFER, weaponDrawOffset+expBarSize[1]))
			weaponDrawOffset += playerWeapon.tileList[0].get_height()
		else:
			weaponDrawOffset += BUFFER

def drawMouse(mousePos):
	screen.blit(mouseCursor, (mousePos[0]-mouseCursor.get_width()//2, mousePos[1]-mouseCursor.get_height()//2 ))
			


def goOverworld(player):
	global screen
	fullscreen = False

	expBar = parseImage(gameConfig["EXP_BAR"][0], (0,0), (int(gameConfig["EXP_BAR"][1]),int(gameConfig["EXP_BAR"][2])), 0, -1, 1)
	healthBar = parseImage(gameConfig["HEALTH_BAR"][0], (0,0), (int(gameConfig["HEALTH_BAR"][1]),int(gameConfig["HEALTH_BAR"][2])), 0, -1, 1)

	difficulty = 1
	level = Level(gameConfig["LEVEL_ROTATION"][0], screen, Person(player, (0,0)), difficulty)
	multiplier = 1

	mousePos = (0,0)
	movingPos = (0,0)

	currentLevel = 0
	achievedWin = False

	goMessageScreen(["Level " + str(currentLevel+1) + "_" + str(difficulty), "Get ready!"], -1)

	stop = False
	while stop == False:		#Go until we quit
		level.update(mousePos)
		level.draw()
		drawHUD(level, expBar, healthBar)
		if drawCustomMouse:
			drawMouse(mousePos)
		drawToWindow(screen)

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
			goMessageScreen(["Level " + str(currentLevel+1) + "_" + str(difficulty), "Get ready!"], -1)
			level = Level(gameConfig["LEVEL_ROTATION"][currentLevel], screen, level.player, difficulty)

		level.player.go( movingPos )

		stop = not level.player.alive
		#Get the keyboard for movement, stuff that is always happens when key is pressed
		movingPos = [0,0]
		keyboardPressed = pygame.key.get_pressed()
		if keyboardPressed[pygame.K_LEFT] or keyboardPressed[pygame.K_a]:
			movingPos = movingPos[0] - 1, movingPos[1]
		if keyboardPressed[pygame.K_RIGHT] or keyboardPressed[pygame.K_d]:
			movingPos = movingPos[0] + 1, movingPos[1] 
		if keyboardPressed[pygame.K_UP] or keyboardPressed[pygame.K_w]:
			movingPos = movingPos[0], movingPos[1] - 1
		if keyboardPressed[pygame.K_DOWN] or keyboardPressed[pygame.K_s]:
			movingPos = movingPos[0], movingPos[1] + 1

		#Get the mouse and keyboard things that happen once per event
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				userInput = pygame.key.name(event.key)
				if userInput == "e":
					level.player.pickupWeapon()
				elif userInput == "space":
					level.player.cycleWeapons()
				elif userInput == "q":
					level = Level(gameConfig["LEVEL_ROTATION"][currentLevel], screen, level.player, 19)
				elif userInput == "r":
					level.player.exp += 1
				elif userInput == "f":
					fullscreen = False if fullscreen else True
					if fullscreen:
						windowScreen = pygame.display.set_mode( (screenSize[0]*screenSizeMultiplier,screenSize[1]*screenSizeMultiplier), pygame.FULLSCREEN )
					else:
						windowScreen = pygame.display.set_mode( (screenSize[0]*screenSizeMultiplier,screenSize[1]*screenSizeMultiplier) )
				elif userInput == "escape":
					stop = True
			if event.type == MOUSEMOTION:
				#Make mouse coords equal to the screen coords
				mousePos = event.pos[0]//screenSizeMultiplier,event.pos[1]//screenSizeMultiplier
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:
					level.player.fireWeapon()
				elif event.button == 2:
					print("What do you want middle click to do anyway?")
				elif event.button == 3:
					print("No special yet....")
			elif event.type == QUIT:
				stop = True

		clock.tick(60)

	if achievedWin:
		goMessageScreen(" ".join(gameConfig["WIN_DEATH_MESSAGE"]), -1)
		goMenu()
	else:
		goMessageScreen(" ".join(gameConfig["DEATH_MESSAGE"]), -1)
		goMenu()

goTitleScreen() #Run our menu to start
