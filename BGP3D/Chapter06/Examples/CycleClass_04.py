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
	def move(self, dt):
		mps = self.speed * 1000 / 3600
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
	def bump(self, entry):
		print(entry.getFromNodePath().getPythonTag("owner").name)
		print("has bumped into:")
		print(entry.getIntoNodePath().getPythonTag("owner").name)
		print("")
	def getPos(self, ref = None):
		if(ref == None): return(self.root.getPos())
		else: return(self.root.getPos(ref))