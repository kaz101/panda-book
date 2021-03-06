''' CycleAI Class
This class is an artificial intelligence designed to
control the cycles that the player must race against.
'''
from UtilityFunctions import *

class CycleAI:
	def __init__(self, cycle):
		self.cycle = cycle
		# Stores a reference to the cycle being controlled by the AI.
		
		taskMgr.add(self.runAI, "Run AI")
		# Adds the AI run task to the task manager.
		
		if(self.cycle.uc1 in self.cycle.lanes[0]):
			self.lane = 0
		else:
			self.lane = 1
		# Figures out which lane the cycle is currently in.
		
		self.riskRange = [10, 20]
		self.foresightRange = [3,5]
		# Specifies the ranges for the two random piloting modifiers that need them.
		
		self.laneChangeChance = .5
		# Sets a chance limit for the AI to change lanes when it should. The higher the limit, the
		# greater the chance of changing lanes.
		
		self.laneChangeAttempted = False
		# Sets a variable that indicates if a lane change has been attempted during a specific turn
		# or not.
		
		self.riskMod = 0
		self.foresightMod = 0
		self.newTurnPrep()
		# creates the two random piloting modifiers that are used to make the AI handle each turn
		# differently, so the AI doesn't seem so mechanical. Randomizer is called to provide
		# initial values.
		
		self.newTurn = False
		# Creates a variable to be used in tracking when a cycle enters and leaves a turn.
		
		self.ucF = self.cycle.lanes[self.lane][self.cycle.uc3.index + self.foresightMod]
		# sets the far marker used to scope out upcoming turns.
		
	
	def runAI(self, task):
		if(self.cycle.cycle == None):
			self.cycle = None
			return task.done
			# Removes the reference to the cycle if it is being cleaned up
			# and ends the task.
			
		dt = globalClock.getDt()
		if (dt > .20):
			return task.cont
		# Find the amount of time that has passed since the last frame. If this amount is too large,
		# there's been a hiccup and this frame should be skipped.
		if(self.cycle.active == True):
			self.checkDistantTurn(dt)
			# checks if the AI needs to slow down for a turn.
			
			self.checkNearTurn(dt)
			# checks if the AI needs to turn.
		
		self.cycle.speedCheck(dt)
		# updates the cycle's speed, if necessary.
		
		self.cycle.simDrift(dt)
		# Simulates drift for the AI cycle.
		
		self.cycle.groundCheck(dt)
		# Keeps the cycle at the proper height above the track.
		
		self.cycle.move(dt)
		# moves the cycle.
		
		self.checkMarkers()
		# Checks progress along the track.
		
		self.cycle.bumpCTrav.traverse(render)
		# Checks for collisions caused by the cycle's shield.
				
		return task.cont
# runAI: Performs all the AI functions each frame.

	def	checkDistantTurn(self, dt):
		turnAngle = self.findAngle(self.ucF, self.cycle.cycle)
		# Get the perceived turn angle.
		
		if(turnAngle < 1 and turnAngle > -1): 
			turnAngle = 0
		# If the turn angle is less than a degree, consider it 0.

		if(self.cycle.speed == 0): turnRate = self.cycle.handling
		else: turnRate = self.cycle.handling * (2 - (self.cycle.speed / self.cycle.maxSpeed))
		# Determine turn rate based on speed.
		
		if(self.cycle.speed > 0):
			eta = trueDist(self.cycle.cycle.getPos(render), self.ucF.getPos(render))/ self.cycle.speed
		else:
			eta = 0
		# Calculates an estimated amount of time until the cycle reaches the far marker.
		
		if(self.laneChangeAttempted == False):
		# Checks if the cycle has tried to change lanes yet.
		
			if(turnAngle < -15):		
				if(self.lane != 1):
					self.changeLanes()
			# Attempts to get in the right lane if an upcoming turn is severe enough.
				
				self.laneChangeAttempted = True
				# Indicates that the lane change was attempted, regardless of success.
		
			elif(turnAngle > 15):		
				if(self.lane != 0):
					self.changeLanes()
			# Attempts to get in the left lane if an upcoming turn is severe enough.
				
				self.laneChangeAttempted = True
				# Indicates that the lane change was attempted, regardless of success.
		
		if(turnAngle < 0): 
			turnAngle *= -1
		# If the turn angle is negative it should be made positive.
		
		if(turnAngle > (turnRate + self.riskMod) * eta and eta != 0): 
			self.cycle.adjustThrottle("down", dt)
			# Adjusts the throttle to slow down for curves.
		
		else:
			self.cycle.adjustThrottle("up", dt)
			# If the turn can be handled or there isn't a turn the throttle is adjusted up.
				
		return
# checkTurn: Monitors the track ahead and determines if turning is necessary, how much, and which direction.
# Also changes the target throttle to slow down for turns.

	def	checkNearTurn(self, dt):
		turnAngle = self.findAngle(self.cycle.uc3, self.cycle.cycle)
		# Get the perceived turn angle.
		
		if(turnAngle < 1 and turnAngle > -1): 
			turnAngle = 0
		
		if(self.cycle.speed == 0): turnRate = self.cycle.handling
		else: turnRate = self.cycle.handling * (2 - (self.cycle.speed / self.cycle.maxSpeed))
		# Determine turn rate based on speed.
		
		if(turnAngle < 0): 
			self.cycle.turning = "r"
			turnRate *= -1
		# If it's a right turn, set the turn rate to a negative
			
			if(turnAngle < turnRate * dt): 
				self.cycle.cycle.setH(self.cycle.cycle, turnRate * dt)
				# Turn the cycle based on the turn rate.
				
			else:
				hardness = (turnRate * dt)/ turnAngle
				turnRate *= hardness
				self.cycle.cycle.setH(self.cycle.cycle, turnRate * dt * hardness)
				# Turn the cycle based on a fraction of the turn rate if the needed 
				# adjustment is small.
				
			if(self.newTurn == False):
				self.newTurn = True
			# Turns newTurn to true when the cycle starts turning, if it isn't true already.
				
		elif(turnAngle > 0):
			self.cycle.turning = "l"
			if(turnAngle > turnRate * dt): 
				self.cycle.cycle.setH(self.cycle.cycle, turnRate * dt)
				# Turn the cycle based on the turn rate.
				
			else:
				hardness = (turnRate * dt)/ turnAngle
				turnRate *= hardness
				self.cycle.cycle.setH(self.cycle.cycle, turnRate * dt * hardness)
				# Turn the cycle based on a fraction of the turn rate if the needed 
				# adjustment is small.
				
			if(self.newTurn == False):
				self.newTurn = True
			# Turns newTurn to true when the cycle starts turning, if it isn't true already.
		
		else:
			self.cycle.turning = None
			
			if(self.newTurn == True):
				self.newTurnPrep()
			# Calls newTurnPrep to prep for the next turn.
			
				self.newTurn = False
			# Sets self.newTurn to false so we know that the 
			# prep for the next turn has been handled.
				
		return
# checkTurn: Monitors the track ahead and determines if turning is necessary, how much, and which direction.
# Also changes the target throttle to slow down for turns.

	def newTurnPrep(self):
		self.riskMod = getRandom(self.riskRange[0], self.riskRange[1])
		self.foresightMod = int(getRandom(self.foresightRange[0], self.foresightRange[1]))
		self.laneChangeAttempted = False
		# Generate new modifiers according the specified ranges.
		
		return
# Randomizer: Generates random variables for AI piloting behavior based on the specified ranges.

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

	def changeLanes(self):
		randVal = getRandom(0,1)
		if(randVal < self.laneChangeChance):
		# Generates and checks a random value to give the cycle a chance of changing lanes.
			if(self.lane == 0):
				self.lane = 1
				self.cycle.uc1 = self.cycle.lanes[1][self.cycle.uc1.index]
				self.cycle.uc2 = self.cycle.lanes[1][self.cycle.uc2.index]
				self.cycle.uc3 = self.cycle.lanes[1][self.cycle.uc3.index]
			elif(self.lane == 1):
				self.lane = 0
				self.cycle.uc1 = self.cycle.lanes[0][self.cycle.uc1.index]
				self.cycle.uc2 = self.cycle.lanes[0][self.cycle.uc2.index]
				self.cycle.uc3 = self.cycle.lanes[0][self.cycle.uc3.index]
				
		return
			
	def checkMarkers(self):
		uc1 = self.cycle.uc1
		# Gets a temporary reference to the current uc1.
		
		self.cycle.checkMarkers()
		# Tells the cycle to update its markers if it passed one.
		
		if(uc1 != self.cycle.uc1):
		# If uc1 changed then the cycle updated to new markers, and ucF needs to
		# be updated as well.
		
			farIndex = self.cycle.uc3.index + self.foresightMod
			if(farIndex >= len(self.cycle.lanes[self.lane])):
				farIndex -= len(self.cycle.lanes[self.lane])
			self.ucF = self.cycle.lanes[self.lane][farIndex]
			# Updates ucF according to the foresight modifier. Also causes the ucF
			# index to wrap around back to zero at the end of a lap.
			
		return
			