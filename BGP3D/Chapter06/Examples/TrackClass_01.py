from TrackLanesClass import TrackLanes
from pandac.PandaModules import *

class Track:
	def __init__(self):
		self.track = loader.loadModel("../Models/Track.egg")
		self.track.reparentTo(render)
		
		self.trackLanes = TrackLanes()
		
		self.gravity = 1
		self.groundCol = loader.loadModel("../Models/Ground.egg")
		self.groundCol.reparentTo(render)
		mask = BitMask32.range(1,3)
		mask.clearRange(2,1)
		self.groundCol.setCollideMask(mask)