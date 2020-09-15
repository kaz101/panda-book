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
		
		self.planet = loader.loadModel("../Models/Planet.egg")
		self.planet.reparentTo(render)
		# Loads the model for the planet and places it in the scene.
		
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
		
		self.setupSkySphere()
		# Creates and initializes the sky sphere that serves as a backdrop for the game.
		
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

	def setupSkySphere(self):
		self.skySphere = loader.loadModel(
			"../Models/LinearPinkSkySphere.bam")
		self.skySphere.reparentTo(render)
		# Loads the sky sphere and adds it to the scene.
		
		self.skySphere.setBin('background', 1)
		# Tells Panda3D to render the sky sphere first.
		
		self.skySphere.setDepthWrite(False) 
		# Tells Panda3D to ignore depth when rendering the sky sphere.
		
		self.skySphere.setShaderOff()
		# Turns off automatic shader generation for the sky sphere.
		
		self.skySphere.setAlphaScale(0)
		# Sacles the alpha channel of the skySphere down to 0 to make the
		# bloom filter ignore it.
		
		taskMgr.add(self.skySphereTask, "SkySphere Task")
		# Adds the task that makes the sky sphere move with the camera to
		# the task manager.
		
		return
#setupSkySphere: Loads the sky sphere and prepares it for use.

	def skySphereTask(self, task):
		if(self.skySphere == None):
			return task.done
			# Ends the task if the skySphere has been removed.
		else:
			self.skySphere.setPos(base.camera, 0, 0, 0)
			return task.cont
#skySphereTask: Moves the sky sphere to the position of the camera
# every frame, so the sky sphere doesn't appear to move.

	def destroy(self):
		self.track.removeNode()
		self.planet.removeNode()
		self.groundCol.removeNode()
		self.skySphere.removeNode()
		self.dirLight.removeNode()
		self.ambLight.removeNode()
		self.trackLanes.destroy()
		self.trackLanes = None
		# Removes everything the track placed in the scene graph.
		
		self.skySphere = None
		# sets self.skySphere to None to end the skySphere task.
		
		render.setLightOff()
		# tells the scene to ignore all the lights previously set on it.
		
		return
# destroy: Cleans away all the track components.
		