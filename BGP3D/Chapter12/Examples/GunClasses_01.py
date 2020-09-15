from direct.interval.IntervalGlobal import *
from direct.actor.Actor import Actor
from pandac.PandaModules import *
from UtilityFunctions import *
from ExplosionClasses_02 import *

class MachineGun:
	def __init__(self, cycle, mount, audio3D):
		self.cycle = cycle
		self.name = "JR Martin J59 Jabber"
		
		self.actor = Actor("../Models/MGActor.egg")
		self.model = loader.loadModel("../Models/MachineGun.bam")
		self.actor.reparentTo(mount)
		self.model.reparentTo(self.actor)
		self.flashModel = loader.loadModel("../Models/LaserFlash.bam")
		self.projModel = loader.loadModel("../Models/LaserProj.bam")
		self.projModel.setScale(.25, 1, .25)
		
		self.refNP = self.cycle.trgtrMount.attachNewNode("MGRefNP")
		
		self.muzzle = self.actor.exposeJoint(None,
			"modelRoot", "Muzzle")
		
		self.audio3D = audio3D
		self.fireSfx = self.audio3D.loadSfx("../Sound/LaserShot.wav")
		self.audio3D.attachSoundToObject(self.fireSfx, self.muzzle)
			
		reloadTime = .25
		self.damage = 10
		self.energyCost = 1.25
		
		self.flashLerp = LerpScaleInterval(self.flashModel, 
			reloadTime * .75, Point3(1,1,1), Point3(.1,.1,.1))
		
		self.firePar = Parallel(
			Func(self.checkForHit),
			Func(self.setEffects),
			self.flashLerp)
		
		self.fireSeq = Sequence(self.firePar,
			Func(self.clearEffects),
			Wait(reloadTime * .25))
				
	def fire(self):
		if(self.fireSeq.isPlaying() == False):
			self.fireSeq.start()
			self.fireSfx.play()
			self.cycle.energy -= self.energyCost
		return
		
	def setEffects(self):
		self.flashModel.reparentTo(self.muzzle)
		self.projModel.reparentTo(self.muzzle)
		self.projModel.lookAt(self.refNP.getPos(self.muzzle))
		self.projModel.setSy(trueDist(Point3(0,0,0), 
			self.refNP.getPos(self.muzzle)) * 2)
		return
		
	def clearEffects(self):
		self.flashModel.detachNode()
		self.projModel.detachNode()
		return
		
	def checkForHit(self):
		self.cycle.trgtrCTrav.traverse(render)
		if(self.cycle.trgtrCHan.getNumEntries() > 0):
			self.cycle.trgtrCHan.sortEntries()
			entry = self.cycle.trgtrCHan.getEntry(0)
			# If collisions were detected sort them nearest to far and pull out the first one.
			
			colPoint = entry.getSurfacePoint(render)
			self.refNP.setPos(render, colPoint)
			# Get the collision point and the range to the collision.
			
			pop = Pop(colPoint)
			# Create an explosion at the collision point.
			
			thingHit = entry.getIntoNodePath()
			if(thingHit.hasPythonTag("owner")):
				thingHit.getPythonTag("owner").hit(self.damage)
		else:
			self.refNP.setPos(self.cycle.trgtrCNP, 0, 300, 0)
			pop = Pop(self.cycle.refNP.getPos(render))
			# If no collision was detected, create a pop at a distant point.
		
	def destroy(self):
		self.actor.delete()
		self.model.removeNode()
		self.flashModel.removeNode()
		self.projModel.removeNode()
		self.refNP.removeNode()
		self.cycle = None
		self.flashLerp = None
		self.firePar = None
		self.fireSeq = None
		self.audio3D.detachSound(self.fireSfx)
		return
	
''' 
take in audio3D store reference
pass audio3D to boom
'''
class Cannon:
	def __init__(self, cycle, mount, audio3D):
		self.cycle = cycle
		self.name = "Virtue X-A9 Equalizer"
		self.audio3D = audio3D
		
		self.actor = Actor("../Models/CannonActor.egg")
		self.model = loader.loadModel("../Models/Cannon.bam")
		self.actor.reparentTo(mount)
		self.model.reparentTo(self.actor)
		self.flashModel = loader.loadModel("../Models/LaserFlash.bam")
		self.projModel = loader.loadModel("../Models/LaserProj.bam")
		
		self.refNP = self.cycle.trgtrMount.attachNewNode("CannonRefNP")
		
		self.muzzle = self.actor.exposeJoint(None,
			"modelRoot", "Muzzle")
			
		self.audio3D = audio3D
		self.fireSfx = self.audio3D.loadSfx("../Sound/LaserShot.wav")
		self.audio3D.attachSoundToObject(self.fireSfx, self.muzzle)
			
		reloadTime = 1.5
		self.damage = 75
		self.energyCost = 5
		self.blastR = 10
		
		self.flashLerp = LerpScaleInterval(self.flashModel, 
			reloadTime * .1, Point3(2,2,2), Point3(.2,.2,.2))
		
		self.firePar = Parallel(
			Func(self.checkForHit),
			Func(self.setEffects),
			self.flashLerp)
		
		self.fireSeq = Sequence(self.firePar,
			Func(self.clearEffects),
			Wait(reloadTime * .9))
				
	def fire(self):
		if(self.fireSeq.isPlaying() == False):
			self.fireSeq.start()
			self.fireSfx.play()
			self.cycle.energy -= self.energyCost
		return
		
	def setEffects(self):
		self.flashModel.reparentTo(self.muzzle)
		self.projModel.reparentTo(self.muzzle)
		self.projModel.lookAt(self.refNP.getPos(self.muzzle))
		self.projModel.setSy(trueDist(Point3(0,0,0), 
			self.refNP.getPos(self.muzzle)) * 2)
		return
		
	def clearEffects(self):
		self.flashModel.detachNode()
		self.projModel.detachNode()
		return
		
	def checkForHit(self):
		self.cycle.trgtrCTrav.traverse(render)
		if(self.cycle.trgtrCHan.getNumEntries() > 0):
			self.cycle.trgtrCHan.sortEntries()
			entry = self.cycle.trgtrCHan.getEntry(0)
			# If collisions were detected sort them nearest to far and pull out the first one.
			
			colPoint = entry.getSurfacePoint(render)
			self.refNP.setPos(render, colPoint)
			# Get the collision point and the range to the collision.
			
			boom = Boom(colPoint, self.blastR, self.damage, self.audio3D)
			# Create an explosion at the collision point.
			
		else:
			self.refNP.setPos(self.cycle.trgtrCNP, 0, 300, 0)
			boom = Boom(self.refNP.getPos(render), 
				self.blastR, self.damage, self.audio3D)
			# If no collision was detected, create a boom at a distant point.
		
	def destroy(self):
		self.actor.delete()
		self.model.removeNode()
		self.flashModel.removeNode()
		self.projModel.removeNode()
		self.refNP.removeNode()
		self.cycle = None
		self.flashLerp = None
		self.firePar = None
		self.fireSeq = None
		self.audio3D.detachSound(self.fireSfx)
		return

