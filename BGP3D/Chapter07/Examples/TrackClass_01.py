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
		
		self.setupLight()
		# Calls the method that creates the track's lighting environment.
		
	def setupLight(self):
		primeL = DirectionalLight("prime")
		primeL.setColor(VBase4(.6,.6,.6,1))
		# Creates the primary directional light and sets it's color to 60%. 
		self.dirLight = render.attachNewNode(primeL)
		self.dirLight.setHpr(45,-60,0)
		# Assigns the light to a nodePath and rotates that nodePath to aim the light.
		
		render.setLight(self.dirLight)
		# Sets the directional light to illuminate everything attached to the render node.
		
		ambL = AmbientLight("amb")
		ambL.setColor(VBase4(.2,.2,.2,1))
		self.ambLight = render.attachNewNode(ambL)
		# Creates an ambient light to fill in the shadows and sets it's color to 20%.
		# also places it in a NodePath.
		
		render.setLight(self.ambLight)
		# Sets the ambient light to illuminate the scene.
		
		return
# setupLight: Sets up the light that will represent the sun on our track.