from direct.gui.DirectGui import *
from pandac.PandaModules import *

class Preloader:
	def __init__(self, fonts):
		self.createGraphics(fonts)
		
		self.prepLoadGroup()
		
		self.loaderBar.setTexOffset(self.modTS, .015, 0)
		base.graphicsEngine.renderFrame()
		base.graphicsEngine.renderFrame()
		
		self.itemCount = 0
		
		for M in self.models:
			item = loader.loadModel(M)
			self.itemCount += 1
			progress = self.itemCount / float(self.totalItems)
			self.loaderBar.setTexOffset(self.modTS, 
				-progress  + .015, 0)
			base.graphicsEngine.renderFrame()
			base.graphicsEngine.renderFrame()
			
		self.destroy()
			
	def createGraphics(self, fonts):
		self.modTS = TextureStage("Modulate")
		self.modTS.setMode(TextureStage.MModulate)
		
		self.frame = DirectFrame(frameSize = (-.3, .3, -.2, .2), 
			frameColor = (1,1,1,0),
			parent = base.aspect2d)
		# Creates the frame that will house the Preloader graphics
		
		loaderEgg = loader.loadModel("../Models/EnergyBar.egg")
		self.loaderBG = loaderEgg.find("**/EnergyBG")
		self.loaderBar = loaderEgg.find("**/EnergyBar")
		self.loaderFrame = loaderEgg.find("**/EnergyFrame")
		self.loaderBG.reparentTo(self.frame)
		self.loaderBar.reparentTo(self.loaderBG)
		self.loaderFrame.reparentTo(self.loaderBG)
		self.loaderBG.setPos(0, 0, -.2)
		# Loads the three parts of the loader Bar and places them
		# on the frame.
		
		alpha = loader.loadTexture("../Images/LoaderAlpha.png")
		alpha.setFormat(Texture.FAlpha)
		alpha.setWrapU(Texture.WMClamp)
		# Loads an alpha texture to use as a cut out for the
		# bars.
		
		self.loaderBar.setTexture(self.modTS, alpha)
		# Applies the alpha cut out texture to the loader bar.
		
		self.text = DirectLabel(
			text = "Loading Suicide Jockeys...",
			text_font = fonts["orange"], text_scale = .1, 
			text_fg = (1,1,1,1), relief = None, 
			text_align = TextNode.ACenter,
			parent = self.frame)
		return
# createGraphics: Creates the text and loader bar for the preloader.

	def prepLoadGroup(self):
		self.models = ["../Models/Track.egg",
						"../Models/Planet.egg",
						"../Models/Ground.egg",
						"../Models/LinearPinkSkySphere.bam",
						
						"../Models/TargetCone.bam",
						"../Models/ShieldBar.egg",
						"../Models/SpeedBar.egg",
						"../Models/EnergyBar.egg",

						"../Models/RedCycle.bam",
						"../Models/RedTurr.bam",
						"../Models/YellowCycle.bam",
						"../Models/YellowTurr.bam",
						"../Models/GreenCycle.bam",
						"../Models/GreenTurr.bam",
						"../Models/BlueCycle.bam",
						"../Models/BlueTurr.bam",
						"../Models/Disc.bam",
						
						"../Models/MachineGun.bam",
						"../Models/Cannon.bam",
						"../Models/LaserFlash.bam",
						"../Models/LaserProj.bam",
						
						"../Models/Explosions/Laserburst1.bam",
						"../Models/Explosions/Laserburst2.bam",
						"../Models/Explosions/Laserburst3.bam"]
						
		self.totalItems = len(self.models)
		
		return
# prepLoadGroup: Creates a list containing all of the models that need to be
# loaded and then counts how many there are.

	def destroy(self):
		self.loaderBG.removeNode()
		self.text.destroy()
		self.frame.destroy()