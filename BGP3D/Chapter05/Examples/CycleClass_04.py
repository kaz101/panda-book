from pandac.PandaModules import Vec3

class Cycle:
	def __init__(self, inputManager):
		self.inputManager = inputManager
		self.setupVarsNPs()
		taskMgr.add(self.cycleControl, "Cycle Control")
	def setupVarsNPs(self):
		self.root = render.attachNewNode("Root")
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
		self.root.setPos(2,15,0)
		base.camera.reparentTo(self.dirNP)
		base.camera.setY(base.camera, -5)
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