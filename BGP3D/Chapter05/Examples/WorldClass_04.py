import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject

from TrackClass_01 import Track
from CycleClass_03 import Cycle

class World(DirectObject):
	def __init__(self):
		base.disableMouse()
		base.setBackgroundColor(0, 0, 0)
		self.track = Track()
		self.cycle = Cycle()

		taskMgr.doMethodLater(10, self.debugTask, "Debug Task")
 
	def debugTask(self, task):
		print(taskMgr)
		taskMgr.removeTasksMatching("Cycle Move *")
		return task.again
w = World()
run()