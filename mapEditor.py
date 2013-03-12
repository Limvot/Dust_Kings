from imageAndMapUtil import *

def menu():

	while True:
		print("Editing options:")
		print("1 - Tile edit existing map")
		print("2 - Convert the map into the most current form")
		print("3 - Create basic map from large map image")
		print("4 - Quit")
		userInput = input("Make your selection:")

		if userInput == '4':
			break

		tileImageFileName = input("Please input the file path for the map's tile image:")
		mapFileName = input("Please input the file path of the pickled map file:")
		tileSize = int(input("Please input the pixel width of the tiles:")), int(input("Please input the pixel height of the tiles:"))
		screenSize = int(input("Please input desired x screen size:")), int(input("Please input desired x screen size:"))

		pygame.init()
		screen = pygame.display.set_mode( screenSize )
		pygame.display.set_caption("Awesome map editor!")
		pygame.mouse.set_visible(1)

		if userInput == '1':
			tileEdit(screen, tileImageFileName, mapFileName, tileSize)
		elif userInput == '2':
			mapConvert(screen, tileImageFileName, mapFileName, tileSize)
		elif userInput == '3':
			createMap(screen, tileImageFileName, mapFileName, tileSize)
	
def tileEdit(screen, tileImageFileName, mapFileName, tileSize):

	pygame.key.set_repeat(1,0)

	mapDict, tileList = loadMap(tileImageFileName, mapFileName, tileSize)
	tileList = scaleImageList2x(tileList)	#Scale up the map's tile list because it is stored at half-rez. The function we use does some simple interpoliation.
	tileSize = tileSize[0]*2, tileSize[1]*2
	sectionSize = screen.get_size()[0]//tileSize[0], screen.get_size()[1]//tileSize[1]
	sectionPos = [0,0]
	screenPos = [0,0]
	multiplier = 1

	#Make a center retical/curser marker
	marker = pygame.Surface(tileSize)
	marker.fill( (255,0,255) )
	markerPos = sectionSize[0]//2, sectionSize[1]//2
	markerDrawPos = markerPos[1]*tileSize[0], markerPos[1]*tileSize[1]


	#Setup fonts
	if pygame.font:					#Only if fonts are enabled
		font = pygame.font.Font(None, 16)										#Font size

	multiEdit = False

	stop = False
	while stop == False:		#Go until we quit
		mapSurface = drawMap(mapDict, tileList, tileSize, sectionSize, sectionPos)
		mapArray = pygame.PixelArray(mapSurface)
		mapArray[:(sectionSize[0]*tileSize[0]):tileSize[0],:] = (0,0,0)
		mapArray[:,:(sectionSize[1]*tileSize[1]):tileSize[1]] = (0,0,0)
		mapSurface = mapArray.make_surface()


		screen.blit(mapSurface, (0,0))	#Draw the new map
		screen.blit(marker, markerDrawPos)	#draw the marker

		#Draw the types
		for xPos in range(sectionPos[0], sectionPos[0]+sectionSize[0]):
			for yPos in range(sectionPos[1], sectionPos[1]+sectionSize[1]):
				screen.blit(font.render(str(mapDict.get((xPos,yPos),(0,0))[1]), 1, (10, 10, 10)), ((xPos-sectionPos[0])*tileSize[0], (yPos-sectionPos[1])*tileSize[1]) )


		pygame.display.flip()
		pygame.time.wait(50)
	

		userInput = getInput(15,5)				#Get user input and update variables accordingly
												#We look for input for 15 milliseconds, returing to processor for 5 every time we look
		if userInput != None:
			print(userInput)

			if userInput == "left":
				sectionPos[0] -= multiplier
			elif userInput == "right":
				sectionPos[0] += multiplier
			elif userInput == "up":
				sectionPos[1] -= multiplier
			elif userInput == "down":
				sectionPos[1] += multiplier

			elif userInput == "x":
				multiplier -= 1
			elif userInput == "z":
				multiplier += 1
			elif userInput == "x":
				multiplier -= 1

			elif userInput == "a":
				if multiEdit == True:
					multiEdit = False
				else:
					multiEdit = True


			elif multiEdit == False:
				if userInput[1] == "1":
					mapDict[ (sectionPos[0]+markerPos[0],sectionPos[1]+markerPos[1]) ] = mapDict[ (sectionPos[0]+markerPos[0],sectionPos[1]+markerPos[1]) ] [0], 1
				elif userInput[1] == "2":
					mapDict[ (sectionPos[0]+markerPos[0],sectionPos[1]+markerPos[1]) ] = mapDict[ (sectionPos[0]+markerPos[0],sectionPos[1]+markerPos[1]) ] [0], 2
				elif userInput[1] == "3":
					mapDict[ (sectionPos[0]+markerPos[0],sectionPos[1]+markerPos[1]) ] = mapDict[ (sectionPos[0]+markerPos[0],sectionPos[1]+markerPos[1]) ] [0], 3
			else:
				if userInput[1] == "1":
					newValue = 1
				elif userInput[1] == "2":
					newValue = 2
				elif userInput[1] == "3":
					newValue = 3

				imageKey = mapDict[ (sectionPos[0]+markerPos[0],sectionPos[1]+markerPos[1]) ][0]
				for key in mapDict.keys():
					if mapDict[key][0] == imageKey:
						mapDict[key] = imageKey, newValue


			if userInput == "quit" or userInput == "escape":
				stop = True

	if input("Save? (y/n):") == 'y':
		print("Saving!")
		pickle.dump(mapDict, open(mapFileName, "wb") )
		print("Done!")
	else:
		print("Not saving!")


def mapConvert(screen, tileImageFileName, mapFileName, tileSize):

	titleList = parseImage(tileImageFileName, (0,0), tileSize, 0, -1, 1)
	mapList = pickle.load( open(mapFileName, "rb") )
	mapDict = {}
	for mapTup in mapList:
		mapDict[(mapTup[0], mapTup[1])] = (mapTup[2], 2)

	pickle.dump(mapDict, open(mapFileName, "wb") )



def createMap(screen, tileImageFileName, mapFileName, tileSize):
	numTilesToParse = int(input("Please input the number of tiles to parse in the map:"))
	largeMapFileName = input("Please input the file path of where to load the large map image:")
	
	mapDict, tileList = parseMap(screen, largeMapFileName, (0,0), tileSize, 0, numTilesToParse, 1)
	
	saveTileList(tileList, tileImageFileName, (0,0), tileSize)
	pickle.dump(mapDict, open(mapFileName, "wb") )



#Go menu!
'''
pygame.init()
screen = pygame.display.set_mode( (32,32) )
pygame.display.set_caption("Awesome map editor!")
pygame.mouse.set_visible(1)
for i in range(10):
	print(int(getInput(-1)[1]))
'''
pygame.init()
screen = pygame.display.set_mode( (1000,1000) )
pygame.display.set_caption("Awesome map editor!")
pygame.mouse.set_visible(1)
tileEdit(screen, "data/maps/kanto/kanto.bmp", "data/maps/kanto/kantoMap.pickle", (16,16))

#menu()

'''
kantoList = parseImage("data/kantopokemon.png", (5,5), (69,69), 0, 302, 1)
johtoList = parseImage("data/johtopokemon.PNG", (5,5), (69,69), 0, 198, 1)
hoennList = parseImage("data/hoennpokemon.PNG", (5,5), (69,69), 0, 266, 1)
print(len(kantoList))
print(len(johtoList))
print(len(hoennList))
tileList = kantoList + johtoList + hoennList
saveTileList(tileList, "data/pokemon/pokemon.bmp", (5,5), (69,69))
#saveTileList(kantoList, "data/pokemon/kantoPokemon.bmp", (5,5), (69,69))
#saveTileList(johtoList, "data/pokemon/johtoPokemon.bmp", (5,5), (69,69))
#saveTileList(hoennList, "data/pokemon/hoennPokemon.bmp", (5,5), (69,69))
'''


