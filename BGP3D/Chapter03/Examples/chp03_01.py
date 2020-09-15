import direct.directbase.DirectStart

class World:
	def __init__(self):
		base.setBackgroundColor(0, 0, 0)
		# Sets the background color to black.
		
		self.track = loader.loadModel("../Models/Track.egg")
		self.track.reparentTo(render)
		self.track.setPos(0,0,-5)
		self.cycle1 = loader.loadModel("../Models/Cycle.bam")
		self.cycle1.reparentTo(render)
		self.cycle1.setPos(2,15,0)
		self.cycle2 = loader.loadModel("../Models/Cycle.bam")
		self.cycle2.reparentTo(render)
		self.cycle2.setPos(-2,15,0)
		# Loads the track and 2 cycles, adds them to the scene graph, 
		# and positions them.
		
		print(taskMgr)
		# Outputs a statistic report on the task manager to the command prompt.
		
w = World()
run()