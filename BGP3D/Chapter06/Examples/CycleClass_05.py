from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from CycleAIClass import CycleAI

class Cycle(DirectObject):
	def __init__(self, inputManager, track, startPos, name, ai = None):
		self.inputManager = inputManager
		self.setupVarsNPs(startPos, name)
		self.setupCollisions()
		self.track = track
		# Stores a reference to the track.
		self.lanes = self.track.trackLanes.lanes
		# gets a reference to the lanes on the track, to shorten the variable name.
		
		startingLane = self.track.trackLanes.getNearestMarker(self).lane
		# Gets the lane for the closest marker to the cycle.
		
		self.uc1 = self.lanes[startingLane][0]
		self.uc2 = self.lanes[startingLane][1]
		self.uc3 = self.lanes[startingLane][2]
		# Sets up 3 variables to store references to the 3 up-coming markers on the
		# track, ahead of the cycle. These are used by the AI to steer, and by player
		# cycles to measure progress along the track.
		if(ai == True):
			self.ai = CycleAI(self)
		# if the ai input is passed anything, it won't default to None, and the cycle will create
		# an AI to control itself.
		elif(ai == None):
			taskMgr.add(self.cycleControl, "Cycle Control")
		# If the cycle isn't using an AI, activate player control.
		
	def setupVarsNPs(self, startPos, name):
		self.name = name
		self.root = render.attachNewNode("Root")
		if(startPos == 1):
			self.root.setPos(5,0,0)
		elif(startPos == 2):
			self.root.setPos(-5,-5,0)
		elif(startPos == 3):
			self.root.setPos(5,-10,0)
		elif(startPos == 4):
			self.root.setPos(-5,-15,0)
		self.dirNP = self.root.attachNewNode("DirNP")
		self.refNP = self.root.attachNewNode("RefNP")
		self.dirVec = Vec3(0,0,0)
		self.cycleVec = Vec3(0,0,0)
		self.refVec = Vec3(0,0,0)
		self.speed = 0
		self.throttle = 0
		self.maxSpeed = 200
		self.accel = 25
		self.handling = 20
		self.cycle = loader.loadModel("../Models/Cycle.bam")
		self.cycle.reparentTo(self.root)
		base.camera.reparentTo(self.dirNP)
		base.camera.setY(base.camera, -5)
		self.markerCount = 0
		self.currentLap = 0
		self.freeFall = False
		self.fallSpeed = 0
		self.trackNP = render.attachNewNode(self.name + "_TrackNode")
	def setupCollisions(self):
		self.shieldCN = CollisionNode(self.name + "_ShieldCN")
		self.shieldCN.setPythonTag("owner", self)
		CS1 = CollisionSphere(0, -.025, .75, .785)
		CS2 = CollisionSphere(0, -1.075, .85, .835)
		CS3 = CollisionSphere(0, 1.125, .6, .61)
		self.shieldCN.addSolid(CS1)
		self.shieldCN.addSolid(CS2)
		self.shieldCN.addSolid(CS3)
		self.shieldCN.setIntoCollideMask(BitMask32.range(2,3))
		self.shieldCN.setFromCollideMask(BitMask32.bit(2))
		self.shieldCNP = self.cycle.attachNewNode(self.shieldCN)
		
		self.bumpCTrav = CollisionTraverser()
		self.bumpCTrav.showCollisions(render)
		self.bumpHan = CollisionHandlerPusher()
		self.bumpHan.addCollider(self.shieldCNP, self.root)
		self.bumpHan.addAgainPattern("%fn-again")
		self.bumpCTrav.addCollider(self.shieldCNP, self.bumpHan)
		
		self.accept(self.name + "_ShieldCN-again", self.bump)
		
		self.gRayCN = CollisionNode(self.name + "_GRayCN")
		self.fRay = CollisionRay(0, .5, 10, 0, 0, -1)
		self.bRay = CollisionRay(0, -.5, 10, 0, 0, -1)
		self.gRayCN.addSolid(self.fRay)
		self.gRayCN.addSolid(self.bRay)
		self.gRayCN.setFromCollideMask(BitMask32.bit(1))
		self.gRayCN.setIntoCollideMask(BitMask32.allOff())
		self.gRayCNP = self.cycle.attachNewNode(self.gRayCN)
		#self.gRayNP.show()
		# Creates a collision ray called gRay and points it down. This ray will be used to monitor the track beneath the cycle
		# to keep the cycle a certain distance above the track and to ensure it's pitch and roll are correct.
		
		self.gCTrav = CollisionTraverser()
		self.gHan = CollisionHandlerQueue()
		self.gCTrav.addCollider(self.gRayCNP, self.gHan)
	def cycleControl(self, task):
		dt = globalClock.getDt()
		if( dt > .20):
			return task.cont
		if(self.inputManager.keyMap["w"] == True):
			self.adjustThrottle("up", dt)
		elif(self.inputManager.keyMap["s"] == True):
			self.adjustThrottle("down", dt)
		if(self.inputManager.keyMap["d"] == True):
			self.turn("r", dt)
		elif(self.inputManager.keyMap["a"] == True):
			self.turn("l", dt)
		if(self.inputManager.keyMap["mouse1"] == True):
			self.cameraZoom("in", dt)
		elif(self.inputManager.keyMap["mouse3"] == True):
			self.cameraZoom("out", dt)
		if(base.mouseWatcherNode.hasMouse() == True):
			mpos = base.mouseWatcherNode.getMouse()
			base.camera.setP(mpos.getY() * 30)
			base.camera.setH(mpos.getX() * -30)
		self.speedCheck(dt)
		self.simDrift(dt)
		self.groundCheck(dt)
		self.move(dt)
		self.bumpCTrav.traverse(render)
		self.checkMarkers()
		return task.cont
	def cameraZoom(self, dir, dt):
		if(dir == "in"): base.camera.setY(base.camera, 10 * dt)
		else: base.camera.setY(base.camera, -10 * dt)
	def turn(self, dir, dt):
		turnRate = self.handling * (2 - 
			(self.speed / self.maxSpeed))
		if(dir == "r"): turnRate = -turnRate
		self.cycle.setH(self.cycle, turnRate * dt)
	def adjustThrottle(self, dir, dt):
		if(dir == "up"):
			self.throttle += .25 * dt
			if(self.throttle > 1 ): self.throttle = 1
		else:
			self.throttle -= .25 * dt
			if(self.throttle < -1 ): self.throttle = -1
	def speedCheck(self, dt):
		if(self.freeFall == False):
			tSetting = (self.maxSpeed * self.throttle)
			if(self.speed < tSetting):
				if((self.speed + (self.accel * dt)) > tSetting):
					self.speed = tSetting
				else:
					self.speed += (self.accel * dt)
			elif(self.speed > tSetting):
				if((self.speed - (self.accel * dt)) < tSetting):
					self.speed = tSetting
				else:
					self.speed -= (self.accel * dt)
		else:
			self.speed -= (self.speed * .125) * dt
	def simDrift(self, dt):
		self.refNP.setPos(self.dirNP, 0, 1, 0)
		self.dirVec.set(self.refNP.getX(), self.refNP.getY(), 0)
		self.refNP.setPos(self.cycle, 0, 1, 0)
		self.cycleVec.set(self.refNP.getX(), self.refNP.getY(), 0)
		self.refVec.set(0,0,1)
		vecDiff = self.dirVec.signedAngleDeg(self.cycleVec, 
			self.refVec)
		if(vecDiff < .1 and vecDiff > -.1):
			self.dirNP.setHpr(self.cycle.getH(), 0, 0)	
		else: self.dirNP.setHpr(self.dirNP, vecDiff * dt * 2.5, 0, 0)
		self.dirNP.setP(self.cycle.getP())
		self.dirNP.setR(0)
	def groundCheck(self, dt):
		self.gCTrav.traverse(render)
		# Intitiate the ground ray traverser.
		points = [None, None]
		if(self.gHan.getNumEntries() > 1):
			self.gHan.sortEntries()
			for E in range(self.gHan.getNumEntries()):
				entry = self.gHan.getEntry(E)
				if(entry.getFrom() == self.fRay and points[0] == None): 
					points[0] = entry.getSurfacePoint(render)
				elif(entry.getFrom() == self.bRay and points[1] == None): 
					points[1] = entry.getSurfacePoint(render)
			# Get the surface contact points for the nearest 2 collisions, which will correspond to the 2 rays.
			# Put them into the points list in a particular order so they are easy to make sense of.			
			
			
		if(points[0] == None or points[1] == None):
			self.teleport()
			return
		else:
			# If either ray didn't collide with the ground, teleport back onto the center of the track.
			
			if(self.freeFall == False):
				self.refNP.setPos(points[1])
				self.refNP.lookAt(points[0])
				pDiff = self.refNP.getP()- self.cycle.getP()
				if(pDiff < .1 and pDiff > -.1):
					self.cycle.setP(self.refNP.getP())
				else:
					self.cycle.setP(self.cycle, pDiff * dt * 5)
			# When not in free fall, find the pitch between the two collision points and smoothly match the cycle to it.
			elif((self.cycle.getP() - (dt * 10)) > -15): 
				self.cycle.setP(self.cycle, -(dt * 10))
			else: 
				self.cycle.setP(-15)
			# In free fall, let the pitch of the cycle slowly drop.
			
			if(self.speed >= 0): 
				self.trackNP.setPos(points[0].getX(), 
					points[0].getY(), points[0].getZ())
			else: 
				self.trackNP.setPos(points[1].getX(), 
					points[1].getY(), points[1].getZ())
			# Set the track node at the collision point on the leading end of the cycle.
			
			height = self.root.getZ(self.trackNP)
			# Get the height of the root node as seen from the track node.
			if(height > 2 and self.freeFall == False): 
				self.freeFall = True
				self.fallSpeed = 0
			# If the height is greater than 2, enter a free fall state and prep free fall variables.
			if(self.freeFall == True):
				self.fallSpeed += (self.track.gravity * 9.8) * dt
				newHeight = height - (self.fallSpeed * dt)
			# In a free fall state, begin accelerating the fall speed and calculate a new height based on that fall speed.
			else:
				hDiff = 1 - height
				if(hDiff > .01 or hDiff < -.01): 
					newHeight = height + (hDiff * dt * 5)
				else: 
					newHeight = 1
			# If not in a freefall state, calculate a new height that gravitates towards the desired height,
			# or if you're close to the desired height, just set it as the new height.

			if(newHeight >= 0): 
				self.root.setZ(self.trackNP, newHeight)
			# If the new height is greater than or equal to zero, set it as root node's height.
			else: 
				self.root.setZ(self.trackNP, 0)
				self.freeFall = False
			# Otherwise, set the root node to a height of 0, and turn off the free fall state.
			self.cycle.setR(0)
			# Constrain the cycle's roll to 0.
	
		return
	def move(self, dt):
		mps = self.speed * 1000 / 3600 # Convert kph to meters per second
		self.refNP.setPos(self.dirNP, 0, 1, 0)
		self.dirVec.set(self.refNP.getX(), self.refNP.getY(), 
			self.refNP.getZ())
		self.root.setPos(self.root, 
			self.dirVec.getX() * dt * mps, 
			self.dirVec.getY() * dt * mps, 
			self.dirVec.getZ() * dt * mps)
			
	def checkMarkers(self):
		if(self.uc1.checkInFront(self) == True):
		# Checks if the cycle has passed in front of uc1.
		
			self.uc1 = self.uc2
			self.uc2 = self.uc3
			self.uc3 = self.uc2.nextMarker
			# If so, get the next set of markers on the track.
			
			self.markerCount += 1
			# Update the cycle's marker count by one.
			
			if(self.uc1 == self.lanes[0][1] or self.uc1 == self.lanes[1][1]):
				self.currentLap += 1
			# If the cycle just passed the first marker, which is at the finish line, increment the lap count.
			
		return
# Checks if uc1 has been passed, and if so, updates all the markers, marker count, and lap count if needed.
	def teleport(self):
		marker = self.track.trackLanes.getNearestMarker(self)
		markerPos = marker.getPos()
		self.root.setPos(markerPos.getX(), 
			markerPos.getY(), self.root.getZ())
		# Put the cycle back on the track.
		
		self.gCTrav.traverse(render)
		# Intitiate the ground ray traverser.
		points = [None, None]
		if(self.gHan.getNumEntries() > 1):
			self.gHan.sortEntries()
			for E in range(self.gHan.getNumEntries()):
				entry = self.gHan.getEntry(E)
				if(entry.getFrom() == self.fRay and points[0]== None): 
					points[0] = entry.getSurfacePoint(render)
				elif(entry.getFrom() == self.bRay and points[1]== None): 
					points[1] = entry.getSurfacePoint(render)
			# Get the surface contact points for the nearest 2 collisions, which will correspond to the 2 rays.
			# Put them into the points list in a particular order so they are easy to make sense of.
		
			if(self.speed >= 0): 
				self.trackNP.setPos(points[0].getX(), 
					points[0].getY(), points[0].getZ())
			else: 
				self.trackNP.setPos(points[1].getX(), 
					points[1].getY(), points[1].getZ())
			# Set the track node at the collision point on the leading end of the cycle.
			
			self.root.setZ(self.trackNP, 1)
			
		self.dirNP.setHpr(marker.getHpr())
		self.cycle.setHpr(marker.getHpr())
		
		self.speed /= 2
	def bump(self, entry):
		print(entry.getFromNodePath().getPythonTag("owner").name)
		print("has bumped into:")
		print(entry.getIntoNodePath().getPythonTag("owner").name)
		print("")
	def getPos(self, ref = None):
		if(ref == None): return(self.root.getPos())
		else: return(self.root.getPos(ref))