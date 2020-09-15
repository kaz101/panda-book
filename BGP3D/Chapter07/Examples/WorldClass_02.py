''' World Class
This class is the launching point for the game.
This is the file that needs to run to start the game,
and this class creates all the pieces of the game.
'''
import direct.directbase.DirectStart
from direct.filter.CommonFilters import CommonFilters

from TrackClass_01 import Track
from CycleClass_02 import Cycle
from InputManagerClass_00 import InputManager

class World:
	def __init__(self):
		base.disableMouse()
		# Turns off the default mouse-camera controls in Panda3D.
		
		base.setBackgroundColor(0, 0, 0)
		# Sets the background to black.
		
		self.inputManager = InputManager()
		# Creates an InputManager to handle all of the user input in the game.
		
		self.track = Track()
		# Creates the track the cycles will race on.
		
		self.cycle1 = Cycle(self.inputManager, self.track, 1, "Bert", ai = False)
		self.cycle2 = Cycle(self.inputManager, self.track, 2, "Ernie")
		# Creates one uncontrolled cycle, and one player controlled cycle.

		taskMgr.doMethodLater(10, self.debugTask, "Debug Task")
		# Tells the debugTask to run once every ten seconds. The debug task is a good
		# place to put various data print outs about the game to help with debugging.
		
		self.filters = CommonFilters(base.win, base.cam)
		filterok = self.filters.setBloom(blend=(0,0,0,1), 
			desat=-0.5, intensity=3.0, size=2)
		
		render.setShaderAuto()
		# Turns on Panda3D's automatic shader generation.
 
	def debugTask(self, task):
		print(taskMgr)
		# prints all of the tasks in the task manager.
		return task.again
# debugTask: Runs once every ten seconds to print out reports on the games status.
w = World()
run()