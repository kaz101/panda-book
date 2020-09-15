''' Marker Class
This class is used to define the markers placed along the track. These markers are
referenced by multiple parts of the game in order to understand the shape and position
of parts of the track.
'''

from pandac.PandaModules import Vec3

class Marker:
	def __init__(self, pos):
		self.lane = 0
		# Creates a variable to store the number ID of the lane this marker is in.
		self.index = 0
		# Creates a variable to store the number ID of the marker within it's lane.
		
		self.np = render.attachNewNode("MarkerNP")
		self.np.setPos(pos.getX(), pos.getY(), pos.getZ())
		# Creates and positions a proxy NodePath to represent the marker's position in
		# space.
		
		self.nextMarker = None
		self.prevMarker = None
		# Creates variables to store the next and previous markers in the lane.
		
		self.adjMarkers = []
		# Creates a list to reference the markers that are adjacent to this one.
		
		self.facingVec = Vec3(0,1,0)
		self.cycleVec = Vec3(0,0,0)
		# Some functions of the marker will need vectors. This creates them ahead of time.
		
	def getPos(self, ref = None):
		if(ref == None): return(self.np.getPos())
		else: return(self.np.getPos(ref))
		return
# getPos: Returns the position of the marker's NodePath.
		
	def getHpr(self, ref = None):
		if(ref == None): return(self.np.getHpr())
		else: return(self.np.getHpr(ref))
		return
# getHpr: Returns the heading, pitch, and roll of the marker's NodePath.
		
	def setFacing(self):
		nmp = self.nextMarker.getPos()
		self.np.lookAt(nmp.getX(), nmp.getY(), self.np.getPos().getZ())
		return
# setFacing: Forces the marker to face directly toward the next marker in the lane.
		
	def checkInFront(self, cycle):
	
		cyclePos = cycle.root.getPos(self.np)
		self.cycleVec.set(cyclePos.getX(), cyclePos.getY(), self.np.getZ())
		self.cycleVec.normalize()
		# Gets the directional vector to the cycle and normalizes it.
		
		cycleAngle = self.facingVec.angleDeg(self.cycleVec)
		# Gets the angle between the marker's facing and the direction to the cycle.
		
		if(cycleAngle > 90): return(False)
		else: return(True)
# checkInFront: Returns True if the given cycle is in front of the marker or False if it is behind it.
		
	def destroy(self):
		self.np.removeNode()
		return
# destroy: Removes the marker's NodePath from the scene.
