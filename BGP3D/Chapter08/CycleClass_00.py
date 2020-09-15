''' Cycle Class
Each instance of this class will be one of the cycles
racing on the track. This class handles all of the
variables and components necessary for a cycle controlled
by the player.

In addition, there is an option to have this class create
an instance of the CycleAI class to control it, instead of
using player input.
'''

from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from CycleAIClass import CycleAI

class Cycle(DirectObject):
	def __init__(self, inputManager, track, startPos, name, ai = None):
		self.inputManager = inputManager
		# Stores a reference to the InputManager to access user input.
		
		self.setupVarsNPs(startPos, name)
		self.setupCollisions()
		# Sets up initial variables, NodePaths, and collision objects.
		
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
		# With this set up, if AI == False, the cycle will be completely uncontrolled.
		
		self.setupLight()
		# Calls the method that creates a light to represent the glow of the cycle's discs and engine.
		
	def setupVarsNPs(self, startPos, name):
		self.name = name
		# Stores a unique name for this cycle.
		
		self.root = render.attachNewNode("Root")
		# Creates and stores the NodePath that will be used as the root of the cycle
		# for the purpose of movement.
		
		if(startPos == 1):
			self.root.setPos(5,0,0)
			self.cycle = loader.loadModel("../Models/RedCycle.bam")
		elif(startPos == 2):
			self.root.setPos(-5,-5,0)
			self.cycle = loader.loadModel("../Models/BlueCycle.bam")
		elif(startPos == 3):
			self.root.setPos(5,-10,0)
			self.cycle = loader.loadModel("../Models/GreenCycle.bam")
		elif(startPos == 4):
			self.root.setPos(-5,-15,0)
			self.cycle = loader.loadModel("../Models/YellowCycle.bam")
		# Sets the root to a new position according to what place it is given.

		self.dirNP = self.root.attachNewNode("DirNP")
		self.refNP = self.root.attachNewNode("RefNP")
		# Creates and stores two more NodePaths, one to track the direction the cycle
		# is moving in and another to use as a reference during various calculations
		# the cycle performs.
		
		self.dirVec = Vec3(0,0,0)
		self.cycleVec = Vec3(0,0,0)
		self.refVec = Vec3(0,0,0)
		# Creates and stores 3 vector objects to be used in simulating drift when the
		# cycle turns.
		
		self.speed = 0
		self.throttle = 0
		self.maxSpeed = 200
		self.accel = 25
		self.handling = 25
		# Sets basic variables for the cycle's racing attributes.
		
		self.cycle.reparentTo(self.root)
		# Loads the visual model for the cycle and reparents it to the root.
		
		base.camera.reparentTo(self.dirNP)
		base.camera.setPos(base.camera, 0, -5, 1)
		# Connects the camera to dirNP so the camera will follow and 
		# rotate with that node. Also moves it backward 5 meters.
		
		self.markerCount = 0
		self.currentLap = 0
		# Creates two variables that will be used to track the progress
		# of the cycle on the track.
		
		self.freeFall = False
		self.fallSpeed = 0
		# Creates two variables to assist with managing the cycle's falls from
		# hills and ramps. 
		self.trackNP = render.attachNewNode(self.name + "_TrackNode")
		# Creates a NodePath to use when setting the cycle's height above the track.
		# refNP won't serve for this purpose, because it exists in root's coordinate space.
		# We need a NodePath in render's coordinate space for this purpose.
		return
# setupVarsNPs: Initializes most of the non-collision variables and NodePaths needed by the cycle.
		
	def setupCollisions(self):
		self.shieldCN = CollisionNode(self.name + "_ShieldCN")
		# Creates a CollisionNode to store the 3 CollisionSpheres that represent the
		# invisible energy shield surrounding the cycle.
		
		self.shieldCN.setPythonTag("owner", self)
		# Connects a reference to the instance of this class to the shield CollisionNode.
		# This will make it much easier to identify this cycle when its shield is struck.
		
		CS1 = CollisionSphere(0, -.025, .75, .785)
		CS2 = CollisionSphere(0, -1.075, .85, .835)
		CS3 = CollisionSphere(0, 1.125, .6, .61)
		self.shieldCN.addSolid(CS1)
		self.shieldCN.addSolid(CS2)
		self.shieldCN.addSolid(CS3)
		# Creates the 3 CollisionSpheres that make up the shield and adds them into
		# the CollisionNode.
		
		self.shieldCN.setIntoCollideMask(BitMask32.range(2,3))
		self.shieldCN.setFromCollideMask(BitMask32.bit(2))
		# Sets the BitMasks on the CollisionNode. The From mask has bit 2 turned on, so
		# the shield can bump into things on bit 2. The Into mask has bits 2, 3, and 4 turned
		# on so the shield can be struck by things on bit 2 (other cycles), 3 (guns), and 4 (explosions)
		
		self.shieldCNP = self.cycle.attachNewNode(self.shieldCN)
		# Connects the shield and its 3 spheres to the cycle model and gets a NodePath to
		# the shield.
		
		self.bumpCTrav = CollisionTraverser()
		self.bumpHan = CollisionHandlerPusher()
		# Creates a CollisionTraverser and a Pusher-type handler to detect and manage
		# collisions caused by the cycle's shield.
		
		self.bumpHan.addCollider(self.shieldCNP, self.root)
		# Tells the pusher handler to push back on self.root when self.shieldCNP is
		# involved in a collision.
		
		self.bumpHan.addAgainPattern("%fn-again")
		# Tells the pusher handler to create an event using the From CollisionNode's
		# name when it handles recurring collisions.
		
		self.bumpCTrav.addCollider(self.shieldCNP, self.bumpHan)
		# Registers the shield and the handler with the traverser.
		
		self.accept(self.name + "_ShieldCN-again", self.bump)
		# Registers the event that the pusher handler will generate and connects it to
		# the bump method.
		
		self.gRayCN = CollisionNode(self.name + "_GRayCN")
		# Creates a second CollisionNode to store the rays that will be used for collision
		# with the ground.
		
		self.fRay = CollisionRay(0, .5, 10, 0, 0, -1)
		self.bRay = CollisionRay(0, -.5, 10, 0, 0, -1)
		# Creates two rays 10 meters up and points them downward. This time we keep a 
		# reference to the rays because we will need them when organizing their collision data.
		
		self.gRayCN.addSolid(self.fRay)
		self.gRayCN.addSolid(self.bRay)
		# Adds the rays to the CollisionNode.
		
		self.gRayCN.setFromCollideMask(BitMask32.bit(1))
		self.gRayCN.setIntoCollideMask(BitMask32.allOff())
		# Sets the BitMasks for gRayCN. The From mask has bit 1 on so it can cause collisions
		# with the ground. The Into mask is turned off completely, because rays should never
		# be collided into.
		
		self.gRayCNP = self.cycle.attachNewNode(self.gRayCN)
		# Attaches the gRayCN to the cycle and gets a NodePath to it.
		
		self.gCTrav = CollisionTraverser()
		self.gHan = CollisionHandlerQueue()
		self.gCTrav.addCollider(self.gRayCNP, self.gHan)
		# Creates a traverser and a Queue-type handler to detect and manage the rays' collisions.
		# Then registers gRayCNP and the handler with the traverser.
		return
# setupCollisions: Preps CollisionNodes, collision solids, traversers, and handlers to get them
# ready for use.
	def setupLight(self):
		self.glow = self.cycle.attachNewNode(
			PointLight(self.name + "Glow"))
		self.glow.node().setColor(Vec4(.2,.6,1,1))
		# Creates a point light on the cycle and sets it's color to a blue-white. 
		
		self.glow.node().setAttenuation(Vec3(0,0,.75))
		# Sets the attenuation on the point light. This controls the fall-off.
		
		render.setLight(self.glow)
		# Sets the light to illuminate the scene.
		return
# setupLight: Creates a point light to represent the glow of the cycle and sets its attributes. Then
# sets the light to illuminate the scene.
		
	def cycleControl(self, task):
		dt = globalClock.getDt()
		if( dt > .20):
			return task.cont
		# Gets the amount of time that has passed since the last frame from the global clock.
		# If the value is too large, there has been a hiccup and the frame will be skipped.
		
		if(self.inputManager.keyMap["up"] == True):
			self.adjustThrottle("up", dt)
		elif(self.inputManager.keyMap["down"] == True):
			self.adjustThrottle("down", dt)
		# Checks the InputManager for throttle control initiated by the user and performs
		# the adjustments.
		
		if(self.inputManager.keyMap["right"] == True):
			self.turn("r", dt)
		elif(self.inputManager.keyMap["left"] == True):
			self.turn("l", dt)
		# Checks the InputManager for turning initiated by the user and performs it.
		
		if(self.inputManager.keyMap["mouse1"] == True):
			self.cameraZoom("in", dt)
		elif(self.inputManager.keyMap["mouse3"] == True):
			self.cameraZoom("out", dt)
		# Checks the InputManager for mouse presses and responds to them.
		
		if(base.mouseWatcherNode.hasMouse() == True):
			mpos = base.mouseWatcherNode.getMouse()
			base.camera.setP(mpos.getY() * 30)
			base.camera.setH(mpos.getX() * -30)
		# Determines if the mouse cursor is in the Panda Window and, if so, uses its
		# position to rotate the camera.
		
		self.speedCheck(dt)
		self.simDrift(dt)
		self.groundCheck(dt)
		self.move(dt)
		self.checkMarkers()
		# Calls the methods that control cycle behavior frame-by-frame.
		
		self.bumpCTrav.traverse(render)
		# Checks for collisions caused by the cycle's shield.
		
		return task.cont
# cycleControl: Manages the cycle's behavior when under player control.

	def cameraZoom(self, dir, dt):
		if(dir == "in"): base.camera.setY(base.camera, 10 * dt)
		else: base.camera.setY(base.camera, -10 * dt)
		return
# cameraZoom: Moves the camera toward or away from the cycle at a rate of 10
# meters per second.

	def turn(self, dir, dt):
		turnRate = self.handling * (2 - 
			(self.speed / self.maxSpeed))
		# Determines the current turn rate of the cycle according to its speed.
		
		if(dir == "r"): turnRate = -turnRate
		# If this is a right turn, then turnRate should be negative.
		
		self.cycle.setH(self.cycle, turnRate * dt)
		# Rotates the cycle according to the turnRate and time.
		
		return
# turn: Rotates the cycle based on its speed to execute turns.

	def adjustThrottle(self, dir, dt):
		if(dir == "up"):
			self.throttle += .25 * dt
			# Increases the throttle setting at a rate of 25% per second.
			if(self.throttle > 1 ): self.throttle = 1
			# Limits the throttle to a maximum of 100%
		else:
			self.throttle -= .25 * dt
			# Decreases the throttle setting at a rate of 25% per second.
			if(self.throttle < -1 ): self.throttle = -1
			# Limits the throttle to a minimum of 100%
		return
# adjustThrottle: Increases or decreases the throttle.

	def speedCheck(self, dt):
		if(self.freeFall == False):
		# The cycle can't accelerate or deccelerate under it's own power if
		# it's in freefall, so we check to make sure it isn't.
		
			tSetting = (self.maxSpeed * self.throttle)
			# Gets the KpH value that corresponds to the current throttle setting.
			
			if(self.speed < tSetting):
			# Checks if the speed is too low.
				if((self.speed + (self.accel * dt)) > tSetting):
				# If so, check if accelerating at the normal rate would raise speed too high.
					self.speed = tSetting
					# If so, just set the speed to the throttle setting.
				else:
					self.speed += (self.accel * dt)
				# If accelerating won't raise the speed too high, go ahead and accelerate.
				
			elif(self.speed > tSetting):
			# Checks if the speed is too high.
				if((self.speed - (self.accel * dt)) < tSetting):
				# If so, check if decelerating at the normal rate would lower speed too much.
					self.speed = tSetting
					# If so, just set the speed to the throttle setting.
				else:
					self.speed -= (self.accel * dt)
				# If decelerating won't loser the speed too much, go ahead and decelerate.
		else:
			self.speed -= (self.speed * .125) * dt
		# If the cycle is in freefall, lower it's speed by 12.5% per second to simulate loss
		# of momentum to friction.
		return
# speedCheck: Controls the speed at which the cycle is moving by adjusting it according to the
# throttle, or degrading it over time when in freefall.

	def simDrift(self, dt):
		self.refNP.setPos(self.dirNP, 0, 1, 0)
		self.dirVec.set(self.refNP.getX(), self.refNP.getY(), 0)
		# Uses refNP to get a vector that describes the facing of dirNP. The height value is
		# discarded as it is unnecessary.
		
		self.refNP.setPos(self.cycle, 0, 1, 0)
		self.cycleVec.set(self.refNP.getX(), self.refNP.getY(), 0)
		# Uses refNP to get a vector that describes the facing of the cycle. The height value is
		# discarded as it is unnecessary.
		
		self.refVec.set(0,0,1)
		# Sets refVec to point straight up. This vector will be the axis used to determine the
		# difference in the angle between dirNP and the cycle.
		
		vecDiff = self.dirVec.signedAngleDeg(self.cycleVec, 
			self.refVec)
		# Gets a signed angle that describes the difference between the facing of dirNP and
		# the cycle.
		
		if(vecDiff < .1 and vecDiff > -.1):
			self.dirNP.setHpr(self.cycle.getH(), 0, 0)
		# if the difference between the two facings is insignificant, set dirNP to face the
		# same direction as the cycle.
		
		else: self.dirNP.setHpr(self.dirNP, vecDiff * dt * 2.5, 0, 0)
		# If the difference is significant, tell dirNP to slowly rotate to try and catch up
		# to the cycle's facing.
		
		self.dirNP.setP(self.cycle.getP())
		self.dirNP.setR(0)
		# Constrains dirNP pitch and roll to the cycle and 0, respectively.
		
		return
# simDrift: This function simulates the cycle drifting when it turns by causing the dirNP, which 
# faces the direction the cycle is moving in, to slowly catch up to the actual facing of the cycle
# over time.

	def groundCheck(self, dt):
		self.gCTrav.traverse(render)
		# Checks for collisions between the ground and the CollisionRays attached to the cycle.
		
		points = [None, None]
		# Preps a list to hold the data from the collisions.
		
		if(self.gHan.getNumEntries() > 1):
		# Verifies that at least 2 collisions occured. If not, there's no point in checking
		# the collisions because we can't get data from both rays.
		
			self.gHan.sortEntries()
			# Arranges the collision entries in the cues from nearest to furthest.
			
			for E in range(self.gHan.getNumEntries()):
			# Iterates through all the entries in the CollisionHandlerQueue
			
				entry = self.gHan.getEntry(E)
				# Stores the current entry in a temporary variable.
				
				if(entry.getFrom() == self.fRay and points[0] == None): 
				# Checks if this entry is a collision caused by the front ray, and 
				# verifies that we don't have front ray data for this frame yet.
					points[0] = entry.getSurfacePoint(render)
					# Stores the actual point of collision, in the coordinate system of render,
					# in the first slot of the points list.
				elif(entry.getFrom() == self.bRay and points[1] == None):
				# Checks if this entry is a collision caused by the back ray, and 
				# verifies that we don't have back ray data for this frame yet.
					points[1] = entry.getSurfacePoint(render)
					# Stores the actual point of collision, in the coordinate system of render,
					# in the second slot of the points list.			
			
		if(points[0] == None or points[1] == None):
			self.teleport()
			return
		# If either ray didn't collide with the track, the cycle is going out of bounds
		# and needs to be teleported back onto the track.
		
		else:
		# If both rays gave us collision data, we can proceed.	
			
			''' The following segment of code controls the pitch of the cycle '''
			if(self.freeFall == False):
			# Checks if the cycle is in freefall. If it's not, we'll need to make the cycle's
			# pitch match the angle of the track.
				
				self.refNP.setPos(points[1])
				# Sets refNP to the spot on the track where the back ray collided.
				self.refNP.lookAt(points[0])
				# Tells refNP to point at the spot on the track where the front ray collided.
				
				pDiff = self.refNP.getP()- self.cycle.getP()
				# Finds the difference in pitch between refNP and the cycle, which is equivalent
				# to the difference between the cycle's pitch and the angle of the track.
				
				if(pDiff < .1 and pDiff > -.1):
					self.cycle.setP(self.refNP.getP())
				# If the pitch difference is insignificant, set the cycle to match the pitch of
				# refNP.
				
				else:
					self.cycle.setP(self.cycle, pDiff * dt * 5)
				# If the difference is significant, smoothly adjust the cycle's pitch toward the
				# pitch of refNP.
				
			
			elif((self.cycle.getP() - (dt * 10)) > -15): 
				self.cycle.setP(self.cycle, -(dt * 10))
			# If the cycle is in freefall and slowly dropping the pitch won't lower it past -15,
			# go ahead and slowly lower it.
			else: 
				self.cycle.setP(-15)
			# If we're in freefall and the cycle's pitch is to low to drop it any further, lock it
			# to exactly -15.
			''' End pitch control '''
			
			''' The following section of code will control the height of the cycle above the track. '''			
			if(self.speed >= 0): 
				self.trackNP.setPos(points[0].getX(), 
					points[0].getY(), points[0].getZ())
			else: 
				self.trackNP.setPos(points[1].getX(), 
					points[1].getY(), points[1].getZ())
			# Set trackNP at the collision point on the leading end of the cycle.
			
			height = self.root.getZ(self.trackNP)
			# Get the height of root as seen from the trackNP.
			
			if(height > 2 and self.freeFall == False): 
				self.freeFall = True
				self.fallSpeed = 0
			# If the height is greater than 2 and we aren't in freefall,
			# enter a freefall state and prep freefall variables.
			
			if(self.freeFall == True):
				self.fallSpeed += (self.track.gravity * 9.8) * dt
				newHeight = height - (self.fallSpeed * dt)
			# In a freefall state, begin accelerating the fall speed and 
			# calculate a new height based on that fall speed.
			
			else:
				hDiff = 1 - height
			# If not in a freefall state, calculate the difference in the actual height and the
			# desired height.
			
				if(hDiff > .01 or hDiff < -.01): 
					newHeight = height + (hDiff * dt * 5)
				# If the difference is significant, calculate a new height that drifts toward
				# the desired height.
				else: 
					newHeight = 1
				# If you're close to the desired height, just set it as the calculated new height.

			if(newHeight >= 0): 
				self.root.setZ(self.trackNP, newHeight)
			# If the new height is greater than or equal to zero, set it as root's height.
			
			else: 
				self.root.setZ(self.trackNP, 0)
				self.freeFall = False
			# Otherwise, set the root node to a height of 0, and turn off the freefall state.
			''' end of height control code '''
			
			self.cycle.setR(0)
			# Constrain the cycle's roll to 0.
	
		return
# groundCheck: Controls the cycle's pitch and it's height above the track.

	def move(self, dt):
		mps = self.speed * 1000 / 3600 
		# Convert kph to meters per second
		
		self.refNP.setPos(self.dirNP, 0, 1, 0)
		self.dirVec.set(self.refNP.getX(), self.refNP.getY(), 
			self.refNP.getZ())
		# Uses refNP to get a vector describing the direction dirNP is facing.
		
		self.root.setPos(self.root, 
			self.dirVec.getX() * dt * mps, 
			self.dirVec.getY() * dt * mps, 
			self.dirVec.getZ() * dt * mps)
		# Moves root forward according to the direction vector, speed, and time.
		
		return
# move: Controls the forward or backward movement of the cycle.
			
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
# checkMarkers: Checks if the nearest marker has been passed, and if so, 
# updates all the markers, marker count, and lap count if needed.

	def teleport(self):
		marker = self.track.trackLanes.getNearestMarker(self)
		markerPos = marker.getPos()
		self.root.setPos(markerPos.getX(), 
			markerPos.getY(), self.root.getZ())
		# Put the cycle back on the track.
		
		self.gCTrav.traverse(render)
		# Checks for collisions between the ground and the CollisionRays attached to the cycle.
		
		points = [None, None]
		# Preps a list to hold the data from the collisions.
		
		if(self.gHan.getNumEntries() > 1):
		# Verifies that at least 2 collisions occured. If not, there's no point in checking
		# the collisions because we can't get data from both rays.
		
			self.gHan.sortEntries()
			# Arranges the collision entries in the cues from nearest to furthest.
			
			for E in range(self.gHan.getNumEntries()):
			# Iterates through all the entries in the CollisionHandlerQueue
			
				entry = self.gHan.getEntry(E)
				# Stores the current entry in a temporary variable.
				
				if(entry.getFrom() == self.fRay and points[0] == None): 
				# Checks if this entry is a collision caused by the front ray, and 
				# verifies that we don't have front ray data for this frame yet.
					points[0] = entry.getSurfacePoint(render)
					# Stores the actual point of collision, in the coordinate system of render,
					# in the first slot of the points list.
				elif(entry.getFrom() == self.bRay and points[1] == None):
				# Checks if this entry is a collision caused by the back ray, and 
				# verifies that we don't have back ray data for this frame yet.
					points[1] = entry.getSurfacePoint(render)
					# Stores the actual point of collision, in the coordinate system of render,
					# in the second slot of the points list.
		
			if(self.speed >= 0): 
				self.trackNP.setPos(points[0].getX(), 
					points[0].getY(), points[0].getZ())
			else: 
				self.trackNP.setPos(points[1].getX(), 
					points[1].getY(), points[1].getZ())
			# Set the track node at the collision point on the leading end of the cycle.
			
			self.root.setZ(self.trackNP, 1)
			# Set the root to a height of 1 above trackNP.
			
		self.dirNP.setHpr(marker.getHpr())
		self.cycle.setHpr(marker.getHpr())
		# Reorients dirNP and the cycle to the same facing as the marker we teleported to.
		
		self.speed /= 2
		# Cuts the speed by half as a penalty for going off the track.
		
		return
# teleport: Moves the cycle back onto the track, fixes its height, and fixes its orientation.

	def bump(self, entry):
		print(entry.getFromNodePath().getPythonTag("owner").name)
		print("has bumped into:")
		print(entry.getIntoNodePath().getPythonTag("owner").name)
		print("")
		return
# bump: Prints a message to the command prompt when the cycle bumps into another cycle.

	def getPos(self, ref = None):
		if(ref == None): return(self.root.getPos())
		else: return(self.root.getPos(ref))
# getPos: returns the position of root in the coordinate system of the given NodePath, if one is given.