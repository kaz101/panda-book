import direct.directbase.DirectStart

from TrackClassHero import Track
from CycleClassHero import Cycle
from InputManagerClass_01 import InputManager

class World:
	def __init__(self):
		base.disableMouse()
		base.setBackgroundColor(0, 0, 0)
		self.inputManager = InputManager()
		self.track = Track()
		self.cycle = Cycle(self.inputManager, self.track, ai = True)

		taskMgr.doMethodLater(10, self.debugTask, "Debug Task")
 
	def debugTask(self, task):
		print(taskMgr)
		taskMgr.removeTasksMatching("Cycle Move *")
		return task.again
w = World()
run()