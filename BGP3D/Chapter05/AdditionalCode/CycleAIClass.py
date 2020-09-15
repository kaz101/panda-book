'''
This file contains several chunks of code. First there are additions to the Cycle class
that will be necessary for the AI to control the cycle, and for measuring a player cycle's
progress around the track.

After that is the block of code contianing the AI class itself.
'''

'''
This section contains code for the Cycle class. Each of these elements can be removed from
this file once they are in the Cycle class.

The first line is the import for the CycleAI class. Place it with the other import line.
'''
from CycleAIClass import CycleAI

'''
Next we have a few updates to the __init__ method of the Cycle class. The def statement for 
the method needs to be replaced with the new one, that accepts additional parameters.
'''
	def __init__(self, inputManager, track, ai = None):
	
'''
This block of code should be added to the __init__method of the Cycle class, right after the
call to setupVarsNPs.
'''

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
		
'''
This last update to __init__ will replace the last line, where the Cycle Control task
is added to the task manager.
'''
		
		if(ai != None):
			self.ai = CycleAI(self)
		# if the ai input is passed anything, it won't default to None, and the cycle will create
		# an AI to control itself.
		else:
			taskMgr.add(self.cycleControl, "Cycle Control")
		# If the cycle isn't using an AI, activate player control.
		
'''
These two lines should be added to the setupVarsNPs method.
'''
	self.markerCount = 0
	self.currentLap = 0

'''
This next function is used by the cycle to evaluate its progress along the track. It should be added to
the Cycle class as is.
'''

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

'''
This is a convenience function for the Cycle class that should be added to it.
'''

	def getPos(self, ref = None):
		if(ref == None): return(self.root.getPos())
		else: return(self.root.getPos(ref))

'''
The last change to Cycle class is this call to checkMarkers, which should be added after the call to move
in the cycleControl method.
'''
		self.checkMarkers()

'''
The remainder of this file is the CycleAI class that will control the cycle as it moves around
the track. Everything above this point needs to be removed for the file to load properly.
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
				
		return task.cont
# Performs all the AI functions each frame.

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
# Monitors the track ahead and determines if turning is necessary, how much, and which direction.
# Also changes the target throttle to slow down for turns.

	def checkThrottle(self, dt):
		
		if(self.cycle.throttle < self.targetThrottle): self.cycle.adjustThrottle("up", dt)
		elif(self.cycle.throttle > self.targetThrottle): self.cycle.adjustThrottle("down", dt)
		# Set the throttle to match the target throttle
		
		return
# Adjusts the throttle when it doesn't match the target throttle.

	def findAngle(self, marker, node):
	
		markPos = marker.getPos(node)
		self.cycle.dirVec.set(markPos.getX(), markPos.getY(), 0)
		self.cycle.dirVec.normalize()
		# Gets the directional vector to the marker and normalizes it.
		
		self.cycle.cycleVec.set(0,1,0)
		# Uses cycleVec for the reference vector.
		
		self.cycle.refVec.set(0,0,1)
		
		return(self.cycle.cycleVec.signedAngleDeg(self.cycle.dirVec, self.cycle.refVec))
# Returns the angle between the node's facing and the direction to the marker.