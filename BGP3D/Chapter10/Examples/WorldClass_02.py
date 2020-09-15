''' World Class
This class is the launching point for the game.
This is the file that needs to run to start the game,
and this class creates all the pieces of the game.
'''

import direct.directbase.DirectStart
from direct.filter.CommonFilters import CommonFilters

from HUDClass_01 import HUD
from RaceClass_02 import Race
from InputManagerClass_01 import InputManager
from MenuClass_00 import Menu


class World:
	def __init__(self):
		base.disableMouse()
		# Turns off the default mouse-camera controls in Panda3D.
		
		base.setBackgroundColor(0, 0, 0)
		# Sets the background to black.
		
		self.inputManager = InputManager()
		# Creates an InputManager to handle all of the user input in the game.

		taskMgr.doMethodLater(10, self.debugTask, "Debug Task")
		# Tells the debugTask to run once every ten seconds. The debug task is a good
		# place to put various data print outs about the game to help with debugging.
		
		self.filters = CommonFilters(base.win, base.cam)
		filterok = self.filters.setBloom(blend=(0,0,0,1), 
			desat=-0.5, intensity=3.0, size=2)
		
		render.setShaderAuto()
		# Turns on Panda3D's automatic shader generation.
		
		self.menuGraphics = loader.loadModel(
			"../Models/MenuGraphics.egg")
		# Loads the egg that contains all the menu graphics.
		
		self.fonts = {
			"silver" : loader.loadFont("../Fonts/LuconSilver.egg"),
			"blue" : loader.loadFont("../Fonts/LuconBlue.egg"),
			"orange" : loader.loadFont("../Fonts/LuconOrange.egg")}
		# Loads the three custom fonts our game will use.
		
		hud = HUD(self.fonts)
		# Creates the HUD.
		
		self.race = Race(self.inputManager, hud)
		self.race.createDemoRace()	
		# creates an instance of the race class and tells it to 
		# start a demo race.
		
		self.createStartMenu()
		# creates the start menu.

		
	def createStartMenu(self):
		menu = Menu(self.menuGraphics, self.fonts, self.inputManager)
			
		menu.initMenu([0,None,
			["New Game","Quit Game"],
			[[self.race.createRace, self.createReadyDialogue],
				[base.userExit]],
			[[None,None],[None]]])
			
	def createReadyDialogue(self):
		menu = Menu(self.menuGraphics, self.fonts, self.inputManager)
			
		menu.initMenu([3,"Are you ready?",
			["Yes","Exit"],
			[[self.race.startRace],[self.race.createDemoRace]],
			[[3],[None]]])
		
	def debugTask(self, task):
		print(taskMgr)
		# prints all of the tasks in the task manager.
		return task.again
# debugTask: Runs once every ten seconds to print out reports on the games status.
w = World()
run()