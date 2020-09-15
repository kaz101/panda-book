''' InputManager Class
The purpose of this class is to have an object
that will record user input and retain that 
information for use by other classes.
'''

from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *

class InputManager(DirectObject):
	def __init__(self):
		self.keyMap = {"up" : False,
						"down" : False,
						"left" : False,
						"right" : False,
						"fire" : False,
						"mouse1" : False,
						"mouse3" : False}
		# Creates a key map to store the state of relevant keyboard keys.
						
		self.accept("w", self.setKey, ["up", True])
		self.accept("s", self.setKey, ["down", True])
		self.accept("a", self.setKey, ["left", True])
		self.accept("d", self.setKey, ["right", True])
		self.accept("enter", self.setKey, ["fire", True])
		self.accept("mouse1", self.setKey, ["mouse1", True])
		self.accept("mouse3", self.setKey, ["mouse3", True])
		# Registers the events for key and mouse presses and 
		# connects them to the setKey method.
		
		self.accept("w-up", self.setKey, ["up", False])
		self.accept("s-up", self.setKey, ["down", False])
		self.accept("a-up", self.setKey, ["left", False])
		self.accept("d-up", self.setKey, ["right", False])
		self.accept("enter-up", self.setKey, ["fire", False])
		self.accept("mouse1-up", self.setKey, ["mouse1", False])
		self.accept("mouse3-up", self.setKey, ["mouse3", False])
		# Registers the events for key and mouse releases and 
		# connects them to the setKey method.
		
		self.setupMouseAim()
		# creates the collision objects used for aiming with the mouse.
		
	def setKey(self, key, value):
		self.keyMap[key] = value
		return
# setKey: stores the given value in the given key within the key map dictionary.

	def setupMouseAim(self):
		self.CN = CollisionNode("RayCN")
		self.cRay = CollisionRay()
		self.CN.addSolid(self.cRay)
		self.CN.setFromCollideMask(BitMask32.bit(8))
		self.CN.setIntoCollideMask(BitMask32.allOff())
		self.CN = base.camera.attachNewNode(self.CN)
		# This creates new collision ray and puts it into a collision node. 
		# It's bitmask is set to 8, and it will be the only collider at bit 8.
		
		self.aimPlaneCN = CollisionNode("aimPlaneCN")
		self.aimPlane = CollisionPlane(Plane(Vec3(0,-1,0), 
			Point3(0,30,0)))
		self.aimPlaneCN.addSolid(self.aimPlane)
		self.aimPlaneCN.setFromCollideMask(BitMask32.allOff())
		self.aimPlaneCN.setIntoCollideMask(BitMask32.bit(8))
		self.aimPlaneCNP = base.camera.attachNewNode(self.aimPlaneCN)
		# This creates an inverted collision sphere and puts it into a collision node. 
		# It's bitmask is set to 8, and it will be the only collidable object at bit 8.
		# The collision node is attached to the camera so that it will move with the camera.
		
		self.cTrav = CollisionTraverser()
		# Creates a traverser to do collision testing
		
		self.cHanQ = CollisionHandlerQueue()
		# Creates a queue type handler to receive the collision event info.
		
		self.cTrav.addCollider(self.CN, self.cHanQ)
		# register the ray as a collider with the traverser, 
		# and register the handler queue as the handler to be used for the collisions.
		
	def getMouseAim(self):
		#This function takes a base node and checks that node and it's children for collision with the mouse ray. It also makes
		#sure that the ray is positioned correctly and aimed at the mouse pointer.
		
		if base.mouseWatcherNode.hasMouse():
			#We must check to make sure the window has the mouse to prevent a crash error caused by accessing the mouse
			#when it's not in the window.
			
			mpos = base.mouseWatcherNode.getMouse()
			#get the mouse position in the window
			
			self.cRay.setFromLens(
				base.camNode, mpos.getX(), mpos.getY())
			#sets the ray's origin at the camera and directs it to shoot through the mouse cursor
			
			self.cTrav.traverse(self.aimPlaneCNP)
			#performs the collision checking pass
			
			self.cHanQ.sortEntries()
			# Sort the handler entries from nearest to farthest
			
			if(self.cHanQ.getNumEntries() > 0):
				entry = self.cHanQ.getEntry(0)
				colPoint = entry.getSurfacePoint(render)
				return(colPoint)