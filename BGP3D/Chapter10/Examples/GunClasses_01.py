from direct.interval.IntervalGlobal import *
from direct.actor.Actor import Actor
from pandac.PandaModules import *
from UtilityFunctions import *

class MachineGun:
	def __init__(self, cycle, mount):
		self.cycle = cycle
		
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
			
		reloadTime = .25
		
		self.flashLerp = LerpScaleInterval(self.flashModel, 
			reloadTime * .75, Point3(1,1,1), Point3(.1,.1,.1))
		
		self.firePar = Parallel(
			Func(self.setEffects),
			self.flashLerp)
		
		self.fireSeq = Sequence(self.firePar,
			Func(self.clearEffects),
			Wait(reloadTime * .25))
				
	def fire(self):
		if(self.fireSeq.isPlaying() == False):
			self.refNP.setPos(0,15,0)
			self.fireSeq.start()
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
		return
