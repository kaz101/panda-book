''' CycleAI Class
This class is an artificial intelligence designed to
control the cycles that the player must race against.
'''

class CycleAI:
	def __init__(self, cycle):
		self.cycle = cycle
		# Stores a reference to the cycle being controlled by the AI.
		
		self.targetThrottle = 0
		# creates a variable for the throttle setting that the AI wishes to be at.
		
		taskMgr.add(self.runAI, "Run AI")
		# Adds the AI run task to the task manager.
	
	def runAI(self, task):
		dt = globalClock.getDt()
		if (dt > .20):
			return task.cont
		# Find the amount of time that has passed since the last frame. If this amount is too large,
		# there's been a hiccup and this frame should be skipped.

		self.checkTurn(dt)
		# checks if the AI needs to turn.
		
		self.checkThrottle(dt)
		# adjusts the throttle to the target throttle.
		
		self.cycle.speedCheck(dt)
		# updates the cycle's speed, if necessary.
		
		self.cycle.simDrift(dt)
		# Simulates drift for the AI cycle.
		
		self.cycle.move(dt)
		# moves the cycle.
		
		self.cycle.checkMarkers()
		# Checks progress along the track.
		
		self.cycle.bumpCTrav.traverse(render)
		# Checks for collisions caused by the cycle's shield.
				
		return task.cont
# runAI: Performs all the AI functions each frame.

	def	checkTurn(self, dt):
		turnAngle = self.findAngle(self.cycle.uc3, self.cycle.cycle)
		# Get the perceived turn angle.
		
		if(turnAngle < 1 and turnAngle > -1): 
			turnAngle = 0
			if(self.targetThrottle < 1):
				self.targetThrottle = 1
		# If the turn angle is less than a degree, consider it 0 and set throttle
		# to maximum.
		
		
		if(self.cycle.speed == 0): turnRate = self.cycle.handling
		else: turnRate = self.cycle.handling * (2 - (self.cycle.speed / self.cycle.maxSpeed))
		# Determine turn rate based on speed.
		
		if(turnAngle < 0): 
			turnRate *= -1
		# If it's a right turn, set the turn rate to a negative
			
			if(turnAngle < turnRate * dt): 
				self.cycle.cycle.setH(self.cycle.cycle, turnRate * dt)
				self.targetThrottle = 1 + (turnRate * dt / self.cycle.handling)
				# Turn the cycle based on the turn rate and adjusts the target throttle
				# to slow down for curves.
				
			else:
				hardness = (turnRate * dt)/ turnAngle
				turnRate *= hardness
				self.cycle.cycle.setH(self.cycle.cycle, turnRate * dt * hardness)
				# Turn the cycle based on a fraction of the turn rate if the needed 
				# adjustment is small.
				
		if(turnAngle > 0):
			if(turnAngle > turnRate * dt): 
				self.cycle.cycle.setH(self.cycle.cycle, turnRate * dt)
				self.targetThrottle = 1 - (turnRate * dt / self.cycle.handling)
				# Turn the cycle based on the turn rate and adjusts the target throttle
				# to slow down for curves.
				
			else:
				hardness = (turnRate * dt)/ turnAngle
				turnRate *= hardness
				self.cycle.cycle.setH(self.cycle.cycle, turnRate * dt * hardness)
				# Turn the cycle based on a fraction of the turn rate if the needed 
				# adjustment is small.
				
		return
# checkTurn: Monitors the track ahead and determines if turning is necessary, how much, and which direction.
# Also changes the target throttle to slow down for turns.

	def checkThrottle(self, dt):
		
		if(self.cycle.throttle < self.targetThrottle): self.cycle.adjustThrottle("up", dt)
		elif(self.cycle.throttle > self.targetThrottle): self.cycle.adjustThrottle("down", dt)
		# Set the throttle to match the target throttle
		
		return
# checkThrottle: Adjusts the throttle when it doesn't match the target throttle.

	def findAngle(self, marker, nodePath):
	
		markPos = marker.getPos(nodePath)
		self.cycle.dirVec.set(markPos.getX(), markPos.getY(), 0)
		self.cycle.dirVec.normalize()
		# Gets the directional vector to the marker and normalizes it.
		
		self.cycle.cycleVec.set(0,1,0)
		# sets cycleVec to equal straight forward.
		
		self.cycle.refVec.set(0,0,1)
		# Sets the reference vector to straight up.
		
		return(self.cycle.cycleVec.signedAngleDeg(self.cycle.dirVec, self.cycle.refVec))
# findAngle: Returns the angle between the NodePath's facing and the direction to the marker.
# The calculation in this method is very similar to how drift is simulated in the cycles.