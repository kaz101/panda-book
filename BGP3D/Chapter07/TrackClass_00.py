''' Track Class
This class stores the data and models for the
track that the cycles race on.
'''
from TrackLanesClass import TrackLanes
from pandac.PandaModules import *

class Track:
	def __init__(self):
		self.track = loader.loadModel("../Models/Track.egg")
		self.track.reparentTo(render)
		# Loads the model for the track and places it in the scene.
		
		self.trackLanes = TrackLanes()
		# Creates the invisible markers that follow the track. These
		# markers are used for many purposes, including tell the AI
		# that controls the cycles when to turn.
		
		self.gravity = 1
		# Sets the percentage of normal earth gravity that will exist on this
		# track. Must be greater than 0 for cycle's to fall. 1 = earth standard.
		
		self.groundCol = loader.loadModel("../Models/Ground.egg")
		self.groundCol.reparentTo(render)
		# Loads the CollisionPolygons that are used to represent the track for
		# collision detection.
		
		mask = BitMask32.range(1,3)
		mask.clearRange(2,1)
		# Creates a BitMask with bits 1 and 3 turned on. We want bits 1 and 3 so that 
		# cycle ground rays and gunshots will collide with the track, and nothing else.
		
		self.groundCol.setCollideMask(mask)
		# Sets the collision mask for the track to the mask we just created.