from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
import random

class Pop:
	def __init__(self, pos):
		rand = random.randint(1,3)
		self.pop = loader.loadModel(
			"../Models/Explosions/Laserburst" + str(rand) + ".bam")
		self.pop.reparentTo(render)
		self.pop.setPos(pos)
		self.pop.find('**/+SequenceNode').node().play(0, 15)
		
		self.self = self
		
		self.seq = Sequence(
			Wait(.5),
			Func(self.destroy))
		
	def destroy(self):
		self.pop.removeNode()
		self.self = None
		return
# destroy: removes the pop graphic from the scene and removes the self reference.
'''
take in audio3D
load and play sound
'''
class Boom:
	def __init__(self, pos, scale, damage, audio3D):
		
		rand = random.randint(1,3)
		self.boom = loader.loadModel(
			"../Models/Explosions/Laserburst" + str(rand) + ".bam")
		self.boom.reparentTo(render)
		self.boom.setPos(pos)
		self.boom.setScale(scale)
		self.boom.find('**/+SequenceNode').node().play(0, 15)
		
		self.self = self
		
		self.seq = Sequence(
			Wait(.5),
			Func(self.destroy))
			
		self.boomCN = CollisionNode("BoomCN")
		self.boomCS = CollisionSphere(0,0,0,scale)
		self.boomCN.addSolid(self.boomCS)
		self.boomCN.setIntoCollideMask(BitMask32.allOff())
		self.boomCN.setFromCollideMask(BitMask32.bit(4))
		self.boomCNP = render.attachNewNode(self.boomCN)
		self.boomCNP.setPos(pos)
		# Creates a collision sphere for the explosion, turns off it's into mask, and sets the from Mask to 4, 
		# which only cycle shields share.
			
		self.boomCTrav = CollisionTraverser()
		self.boomCHan = CollisionHandlerQueue()
		self.boomCTrav.addCollider(self.boomCNP, self.boomCHan)
		# Creates a collision traverser and handler to manage the explosion's collision detection.
		
		self.checkCollision(damage)
		# Checks for cycles in the radius of the blast.
		
		self.audio3D = audio3D
		self.boomSfx = self.audio3D.loadSfx("../Sound/LaserBoom.wav")
		self.audio3D.attachSoundToObject(self.boomSfx, self.boom)
		self.boomSfx.play()
		
	def checkCollision(self, damage):
		cyclesDamaged = []
		self.boomCTrav.traverse(render)
		if(self.boomCHan.getNumEntries() > 0):
			for E in range(self.boomCHan.getNumEntries()):
			# Walk through all the collisions
				entry = self.boomCHan.getEntry(E)
				cycleHit = entry.getIntoNodePath().getPythonTag("owner")
				# Gets the reference to the cycle involved in this collision.
				if(cycleHit not in cyclesDamaged):
					cycleHit.hit(damage)
					cyclesDamaged.append(cycleHit)
				# Since cycles have 3 collision spheres for their shield, it's
				# possible for an explosion to collide with them multiple times.
				# The cyclesDamaged list is used to ensure that each cycle is 
				# only damaged once.

	def destroy(self):
		self.boom.removeNode()
		self.boomCNP.removeNode()
		self.audio3D.detachSound(self.boomSfx)
		self.self = None
		return