import direct.directbase.DirectStart
from pandac.PandaModules import *
from direct.actor.Actor import Actor

class World:
	def __init__(self):
		base.disableMouse()
		
		base.camera.setPos(0, -5, 1)
		
		self.setupLight()
	
		self.kid = Actor("../Models/Kid.egg",
			{"Walk" : "../Animations/Walk.egg"})
		self.kid.reparentTo(render)
		self.kid.loop("Walk")
		self.kid.setH(180)
		
	def setupLight(self):
		primeL = DirectionalLight("prime")
		primeL.setColor(VBase4(.6,.6,.6,1))
		# Creates the primary directional light and sets it's color to 60%. 
		self.dirLight = render.attachNewNode(primeL)
		self.dirLight.setHpr(45,-60,0)
		# Assigns the light to a nodePath and rotates that nodePath to aim the light.
		
		render.setLight(self.dirLight)
		# Sets the directional light to illuminate everything attached to the render node.
		
		ambL = AmbientLight("amb")
		ambL.setColor(VBase4(.2,.2,.2,1))
		self.ambLight = render.attachNewNode(ambL)
		# Creates an ambient light to fill in the shadows and sets it's color to 20%.
		# also places it in a NodePath.
		
		render.setLight(self.ambLight)
		# Sets the ambient light to illuminate the scene.
		
		return
		
		
w = World()
run()
		