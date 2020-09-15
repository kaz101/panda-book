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
		taskMgr.doMethodLater(5, self.cycleMove1, "Cycle Move 1")
		taskMgr.doMethodLater(10, self.debugTask, "Debug Task")
		self.accept("h", self.setKey)
	def setKey(self):
		print("Hello!")
	def cycleMove1(self, task):
		dt = globalClock.getDt()
		if( dt > .20):
			return task.cont
		self.cycle.setY(self.cycle, 10 * dt)
		return task.cont
	def debugTask(self, task):
		print(taskMgr)
		taskMgr.removeTasksMatching("Cycle Move *")
		return task.again
w = World()
run()