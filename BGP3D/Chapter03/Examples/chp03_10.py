import direct.directbase.DirectStart

class World:
	def __init__(self):
		base.setBackgroundColor(0, 0, 0)
		self.track = loader.loadModel("../Models/Track.egg")
		self.track.reparentTo(render)
		self.track.setPos(0,0,-5)
		self.cycle1 = loader.loadModel("../Models/Cycle.bam")
		self.cycle1.reparentTo(render)
		self.cycle1.setPos(2,15,0)
		self.cycle2 = loader.loadModel("../Models/Cycle.bam")
		self.cycle2.reparentTo(render)
		self.cycle2.setPos(-2,15,0)
		taskMgr.doMethodLater(5, self.cycleMove1, "Cycle Move 1")
		taskMgr.doMethodLater(5, self.cycleMove2, "Cycle Move 2")
		taskMgr.doMethodLater(10, self.debugTask, "Debug Task")
	def cycleMove1(self, task):
		dt = globalClock.getDt()
		if( dt > .20):
			return task.cont
		self.cycle1.setY(self.cycle1, 10 * dt)
		return task.cont
	def cycleMove2(self, task):
		dt = globalClock.getDt()
		if( dt > .20):
			return task.cont
		self.cycle2.setY(self.cycle2, 10 * dt)
		return task.cont
	def debugTask(self, task):
		print(taskMgr)
		taskMgr.removeTasksMatching("Cycle Move *")
		return task.again
w = World()
run()