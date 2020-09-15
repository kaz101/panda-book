import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject

class World(DirectObject):
	def __init__(self):
		base.setBackgroundColor(0, 0, 0)
		self.track = loader.loadModel("../Models/Track.egg")
		self.track.reparentTo(render)
		self.track.setPos(0,0,-5)
		self.cycle = loader.loadModel("../Models/Cycle.bam")
		self.cycle.reparentTo(render)
		self.cycle.setPos(2,15,0)
		self.keyMap = {"w" : False,
						"s" : False,
						"a" : False,
						"d" : False}
		taskMgr.add(self.cycleControl, "Cycle Control")
		taskMgr.doMethodLater(10, self.debugTask, "Debug Task")
		self.accept("w", self.setKey, ["w", True])
		self.accept("s", self.setKey, ["s", True])
		self.accept("a", self.setKey, ["a", True])
		self.accept("d", self.setKey, ["d", True])
		self.accept("w-up", self.setKey, ["w", False])
		self.accept("s-up", self.setKey, ["s", False])
		self.accept("a-up", self.setKey, ["a", False])
		self.accept("d-up", self.setKey, ["d", False])
	def setKey(self, key, value):
		self.keyMap[key] = value
	def cycleControl(self, task):
		dt = globalClock.getDt()
		if( dt > .20):
			return task.cont
		if(self.keyMap["w"] == True):
			self.cycle.setY(self.cycle, 10 * dt)
		return task.cont
	def debugTask(self, task):
		print(taskMgr)
		taskMgr.removeTasksMatching("Cycle Move *")
		return task.again
w = World()
run()