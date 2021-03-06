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
		taskMgr.doMethodLater(5, self.cycleMove, "Cycle Move")
		taskMgr.add(self.debugTask, "Debug Task")
	def cycleMove(self, task):
		dt = globalClock.getDt()
		self.cycle1.setY(self.cycle1, 10 * dt)
		return task.cont
	def debugTask(self, task):
		print(taskMgr)
		return task.cont
w = World()
run()