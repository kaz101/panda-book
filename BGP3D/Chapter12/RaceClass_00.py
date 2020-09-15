''' Race Class
This class will own all the components of
a race and control global race status, such
as what ranking cycles are in and whether 
the race is finished or still going.
'''

from pandac.PandaModules import *
from direct.showbase import Audio3DManager
from TrackClass_00 import Track
from CycleClass_00 import Cycle

class Race:
	def __init__(self, inputManager, hud):
	
		self.inputManager = inputManager
		#gets a reference to the inputManager to pass on to the player cycle
		
		self.cycles = []
		# creates a list to store cycles
		
		self.track = None
		# creates a variable to store the track.
		
		self.hud = hud
		# stores a reference to the HUD.
		
		self.amList = []
		self.a3DList = []
		
		for N in range(4):
			self.amList.append(AudioManager.createAudioManager())
			base.addSfxManager(self.amList[N])
			self.a3DList.append(Audio3DManager.Audio3DManager(
				base.sfxManagerList[N + 1], camera))
			self.a3DList[N].setDropOffFactor(.1)
		# Creates 4 AudioManagers for sound effects, one for each cycle.
		# Adds the 4 AudioManagers to the SFX manager list.
		# creates 4 3D audio wrappers with the camera set as a listener
		# Reduces the volume drop off over distance for each 3D audio wrapper.
		
	def createDemoRace(self):
		self.hud.hide()
		# Hides the HUD during the demo.
		
		self.destroyRace()
		# removes any existing race components.
		
		self.track = Track()
		# Creates the track
		
		self.cycles.append(Cycle(self.inputManager, 
			self.track, self.a3DList[0], 1, "Bert", ai = True))
		self.cycles.append(Cycle(self.inputManager, 
			self.track, self.a3DList[1], 2, "Ernie", ai = True))
		self.cycles.append(Cycle(self.inputManager, 
			self.track, self.a3DList[2], 3, "William", ai = True))
		self.cycles.append(Cycle(self.inputManager, 
			self.track, self.a3DList[3], 4, "Patrick", ai = True))
		# Creates 4 AI controlled cycles.
		
		self.setCameraHigh(self.cycles[0])
		# Attaches the camera to one cycle
		
		self.startRace(1)
		# Starts the race after 1 second delay.
		
		return
#createDemoRace: Creates all the components for a demo race.
	
	def createRace(self):
		self.hud.hide()
		# Hides the HUD because cycles are about to be destroyed.
		
		self.destroyRace()
		# removes any existing race components.
		
		self.track = Track()
		# Creates the track
		
		self.cycles.append(Cycle(self.inputManager, 
			self.track, self.a3DList[0], 1, "Bert"))
		self.cycles.append(Cycle(self.inputManager, 
			self.track, self.a3DList[1], 2, "Ernie", ai = True))
		self.cycles.append(Cycle(self.inputManager, 
			self.track, self.a3DList[2], 3, "William", ai = True))
		self.cycles.append(Cycle(self.inputManager, 
			self.track, self.a3DList[3], 4, "Patrick", ai = True))
		# Creates 1 player controlled cycle and 3 AI controlled cycles.
		
		self.hud.setCycle(self.cycles[0])
		self.hud.show()
		# Sets the hude to report on the player cycle, and makes it visible.
		
		self.setCameraFollow(self.cycles[0])
		# Attaches the camera to one cycle
		
		return
#createRace: Creates all the components for a regular race.
		
	def setCameraFollow(self, cycle):
		base.camera.reparentTo(cycle.dirNP)
		base.camera.setPos(0, -15, 3)
		base.camera.setHpr(0,0,0)
		# Connects the camera to dirNP so the camera will follow and 
		# rotate with that node. Also moves it backward 5 meters.
		
		return
# setCameraFollow: sets the camera behind and slightly above a cycle
# and puts it in follow mode.
		
	def setCameraHigh(self, cycle):
		base.camera.reparentTo(cycle.dirNP)
		# Connects the camera to dirNP so the camera will follow and 
		# rotate with that node.
		
		base.camera.setPos(0, 30, 30)
		base.camera.lookAt(cycle.root)
		# Moves the camera ahead of the cycle and up, and then points
		# it at the cycle.
		
		return
# setCameraHigh: sets the camera in front of and above a cycle
# and puts it in follow mode.
	
	def startRace(self, delay):
		taskMgr.doMethodLater(delay, self.startCycles, "Start Cycles")
		return
# startRace: sets up startCycles to be called after a delay.
	
	def startCycles(self, task):
		for C in self.cycles:
			C.active = True
		return task.done
# startCycles: activates the cycles.

	def destroyRace(self):
		if(self.track != None):
			self.track.destroy()
		# If a track already exists, this removes it.
		
		for C in self.cycles:
			C.destroy()
		del self.cycles[0:4]
		# removes any cycles already in existance.
		
		return
# destroyRace: removes any existing race components.
		
		
		
		