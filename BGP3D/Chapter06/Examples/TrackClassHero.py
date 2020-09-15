from TrackLanesClass import TrackLanes

class Track:
	def __init__(self):
		self.track = loader.loadModel("../Models/Track.egg")
		self.track.reparentTo(render)
		self.track.setPos(0,0,-5)
		
		self.trackLanes = TrackLanes()