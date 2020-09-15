from direct.interval.IntervalGlobal import *
import random

class Pop:
	def __init__(self, pos):
		
		rand = random.randint(1,3)
		self.pop = loader.loadModel(
			"../Models/Explosions/Laserburst" + str(rand) + ".bam")
		self.pop.reparentTo(render)
		self.pop.setPos(pos)
		self.pop.find('**/+SequenceNode').node().play(0, 15)
		
		self.self = self
		
		self.seq = Sequence(
			Wait(.5),
			Func(self.destroy))
		
	def destroy(self):
		self.pop.removeNode()
		self.self = None
		return
# destroy: removes the pop graphic from the scene and removes the self reference.