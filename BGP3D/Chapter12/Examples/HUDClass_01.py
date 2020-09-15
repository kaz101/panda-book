from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *

class HUD:
	def __init__(self, fonts):
		self.modTS = TextureStage("Modulate")
		self.modTS.setMode(TextureStage.MModulate)
		# Creats a texture stage to use for making alpha cut outs.
		
		self.createLLHUD(fonts)
		# Creates the lower left corner of the HUD.
		
		self.createURHUD(fonts)
		# Creates the upper right corner of the HUD.
		
		self.createWarning(fonts)
		# Creates the warning message that flashes on the screen when
		# the cycle is in emergency shut down.
		
		self.visible = False
		# a boolean variable that let's the HUD know if it is visible
		# or not.
		
		taskMgr.add(self.updateHUD, "Update HUD")
		# Adds the task that keeps HUD info up to date.
		
	def setCycle(self, cycle):
		self.cycle = cycle
		# stores a reference to the cycle.
		
		self.targetCone = loader.loadModel("../Models/TargetCone.bam")
		self.targetCone.setRenderModeThickness(1)
		self.targetCone.reparentTo(self.cycle.trgtrMount)
		self.targetCone.setColor(1,.25,.25)
		# Loads the targeting cone and attaches it to the cyle's targeter mount.
		
		self.guns = [self.cycle.LMG, self.cycle.RMG,
			self.cycle.cannon]
		# Gets references to the weapons the HUD will be tracking.
		
		self.gunNames[0]["text"] = self.guns[0].name
		self.gunNames[1]["text"] = self.guns[1].name
		self.gunNames[2]["text"] = self.guns[2].name
		# Gets the weapon names to display.
		
		return
# setCycle: sets the cycle that the HUD will report on.
			
	def createLLHUD(self, fonts):
		self.llFrame = DirectFrame(frameSize = (0,.60,0,.45), 
			frameColor = (1, 1, 1, 0), 
			parent = base.a2dBottomLeft)
		# Creates the frame that will house the lower left portion
		# of the HUD.
		
		shieldEgg = loader.loadModel("../Models/ShieldBar.egg")
		self.shieldBG = shieldEgg.find("**/BackgroundBar")
		self.shieldBar = shieldEgg.find("**/ShieldBar")
		self.shieldFrame = shieldEgg.find("**/BarFrame")
		self.shieldBG.reparentTo(self.llFrame)
		self.shieldBar.reparentTo(self.shieldBG)
		self.shieldFrame.reparentTo(self.shieldBG)
		self.shieldBG.setPos(.1,0, .225)
		# Loads the three parts of the Shield Bar and places them
		# on the lower left frame.
		
		speedEgg = loader.loadModel("../Models/SpeedBar.egg")
		self.speedBG = speedEgg.find("**/BackgroundBar")
		self.speedBar = speedEgg.find("**/SpeedBar")
		self.speedFrame = speedEgg.find("**/BarFrame")
		self.speedBG.reparentTo(self.llFrame)
		self.speedBar.reparentTo(self.speedBG)
		self.speedFrame.reparentTo(self.speedBG)
		self.speedBG.setPos(.175,0, .225)
		# Loads the three parts of the Speed Bar and places them
		# on the lower left frame.
				
		alpha = loader.loadTexture("../Images/BarAlpha.png")
		alpha.setFormat(Texture.FAlpha)
		alpha.setWrapV(Texture.WMClamp)
		# Loads an alpha texture to use as a cut out for the
		# bars.
		
		self.speedBar.setTexture(self.modTS, alpha)
		self.shieldBar.setTexture(self.modTS, alpha)
		# Applies the alpha cut out texture to the two bars.
		
		self.throttleBar = speedEgg.find("**/ThrottleBar")
		self.throttleBar.reparentTo(self.speedBG)
		# Loads the throttle marker and puts it on top of the speed bar.
		
		throtAlpha = loader.loadTexture("../Images/ThrottleAlpha.png")
		throtAlpha.setFormat(Texture.FAlpha)
		self.throttleBar.setTexture(self.modTS, throtAlpha)
		# Loads the alpha cut out that constrains the throttle bar
		# within the bar frame, and applies it.
		
		self.shieldText = DirectLabel(text = "500 R", 
			text_font = fonts["blue"], text_scale = .075, 
			pos = (.5, 0, .25), text_fg = (1,1,1,1), 
			relief = None, text_align = TextNode.ARight,
			parent = self.llFrame)
		# Creates a DirectLabel to display the text value of the
		# shield bar.
		
		self.speedText = DirectLabel(text = "180 KPH", 
			text_font = fonts["orange"], text_scale = .075, 
			pos = (.5, 0, .15), text_fg = (1,1,1,1), 
			relief = None, text_align = TextNode.ARight,
			parent = self.llFrame)
		# Creates a DirectLabel to display the text value of the
		# shield bar.	

		return
# createLLHUD: creates all the pieces of the lower left corner of
# the HUD.

	def createURHUD(self, fonts):
		self.urFrame = DirectFrame(frameSize = (-.6, 0, -.4, 0), 
			frameColor = (1,1,1,0),
			parent = base.a2dTopRight)
		# Creates the frame that will house the upper right portion
		# of the HUD.
		
		energyEgg = loader.loadModel("../Models/EnergyBar.egg")
		self.energyBG = energyEgg.find("**/EnergyBG")
		self.energyBar = energyEgg.find("**/EnergyBar")
		self.energyFrame = energyEgg.find("**/EnergyFrame")
		self.energyBG.reparentTo(self.urFrame)
		self.energyBar.reparentTo(self.energyBG)
		self.energyFrame.reparentTo(self.energyBG)
		self.energyBG.setPos(-.35, 0, -.0375)
		# Loads the three parts of the Energy Bar and places them
		# on the upper right frame.
		
		alpha = loader.loadTexture("../Images/ReloadAlpha.png")
		alpha.setFormat(Texture.FAlpha)
		alpha.setWrapU(Texture.WMClamp)
		# Loads an alpha texture to use as a cut out for the
		# bars.
		
		self.energyBar.setTexture(self.modTS, alpha)
		# Applies the alpha cut out texture to the energy bar.
		
		self.energyText = DirectLabel(text = "100",
			text_font = fonts["orange"], text_scale = .05, 
			pos = (-.65, 0, -.0525), text_fg = (1,1,1,1),
			relief = None, text_align = TextNode.ARight,
			parent = self.urFrame)
		# Creates a DirectLabel to display the text value of the
		# energy bar.
		
		self.reloadGreen = loader.loadTexture(
			"../Images/ReloadGreen.png")
		self.reloadRed = loader.loadTexture(
			"../Images/ReloadRed.png")
		# loads the two textures that will be used for the color of the
		# reload bars.
		
		self.reloadBars = []
		self.gunNames = []
		# creates two lists to store the HUD components related to weapons.
		
		for N in range(3):
			self.reloadBars.append(loader.loadModel(
				"../Models/ReloadBar.egg"))
			self.reloadBars[N].reparentTo(self.urFrame)
			self.reloadBars[N].setPos(-.6, 0, -.1125 + (N * -.05))
			self.reloadBars[N].setScale(.1, 0, .1)
			self.reloadBars[N].setTexture(self.modTS, alpha)
			self.reloadBars[N].setTexOffset(self.modTS, .015, 0)
			# creates the reload time bar for the weapon.
		
			self.gunNames.append(DirectLabel(text = "Gun Name",
				text_font = fonts["orange"], text_scale = .035,
				pos = (-.55, 0, -.125 + (N * -.05)),
				text_fg = (1,1,1,1), relief = None,
				text_align = TextNode.ALeft,
				parent = self.urFrame))
			# Creates a DirectLabel to display the name of the weapon.
		
		return
# createURHUD: creates all the pieces of the upper right corner of
# the HUD.
	
	def createWarning(self, fonts):
		self.warning = DirectLabel(
			text = "*** Emergency Shut Down Active ***",
			text_font = fonts["orange"], text_scale = .1, 
			text_fg = (1,1,1,0), relief = None, 
			text_align = TextNode.ACenter,
			parent = base.aspect2d)
			
		self.warningLerp = LerpFunc(self.fadeWarning,
             fromData = 1,
             toData = 0,
             duration = .5)
			 
		self.warningSeq = Sequence(
			Func(self.showWarning),
			Wait(1),
			self.warningLerp,
			Wait(.5))
		
		return
# createWarning: creates the warning message that appears on screen
# when the cycle goes into emergency shut down. Also creates the Intervals
# that are used to control the warning's behavior.

	def updateLLHUD(self):
		if(self.cycle.throttle >= 0):
			self.throttleBar.setColor(0, 1, 0)
			throtRatio = 1 - self.cycle.throttle
		else:
			self.throttleBar.setColor(1, 1, 1)
			throtRatio = 1 + self.cycle.throttle
		# Colors the throttle bar and determines the throtRatio
		# based on whether the throttle is set to forward or
		# reverse.
		
		self.throttleBar.setTexOffset(TextureStage.getDefault(),
				0, .925 * throtRatio)
		# Moves throttle bar's texture according to the throttle 
		# ratio.
			
		if(self.cycle.speed >= 0):
			speedRatio = (self.cycle.maxSpeed - 
				self.cycle.speed) / self.cycle.maxSpeed
		else:
			speedRatio = (self.cycle.maxSpeed + 
				self.cycle.speed) / self.cycle.maxSpeed
		# Determines the speed ratio based on whether the cycle
		# is moving forward or is in reverse.
			
		self.speedBar.setTexOffset(self.modTS, 0, .95 * speedRatio)
		# Moves the alpha cut out texture on the speed bar according
		# to the speed ratio.
		
		shieldRatio = (self.cycle.maxShield - 
			self.cycle.shield) / self.cycle.maxShield
		# Calculates the shield ratio.
		
		self.shieldBar.setTexOffset(self.modTS,	0, .95 * shieldRatio)
		# Moves the alpha cut out texture on the shield bar according
		# to the shield ratio.
		
		self.speedText["text"] = str(int(self.cycle.speed)) + " KPH"
		self.shieldText["text"] = str(int(self.cycle.shield)) + " R"
		# Updates the text values for speed and shield strength.
		
		return
# updateLLHUD: updates all the HUD pieces in the lower left corner.

	def updateURHUD(self):
	
		energyRatio = self.cycle.energy / self.cycle.maxEnergy
		# Determines the energy ratio
		
		self.energyBar.setTexOffset(self.modTS, 
			-(1 - energyRatio) + .015, 0)
		# Moves the alpha cut out texture on the energy bar according
		# to the energy ratio.
		
		self.energyText["text"] = str(int(self.cycle.energy))
		# Updates the text value for the energy
		
		for N in range(3):
		# Iterates through the weapons
		
			if(self.guns[N].fireSeq.isPlaying() == True):
			# checks if the weapon is reloading.
			
				if(self.reloadBars[N].getTexture != self.reloadRed):
					self.reloadBars[N].setTexture(self.reloadRed, 1)
				# turns the reload bar red if it isn't already.
				
				reloadRatio = (self.guns[N].fireSeq.getT()
					/ self.guns[N].fireSeq.getDuration())
				# determines the reload ratio
				
				self.reloadBars[N].setTexOffset(self.modTS,
					-(1 - reloadRatio) + .015, 0)
				# Moves the alpha cut out texture on the reload bar
				# according to the reload ratio
				
			elif(self.reloadBars[N].getTexture() != self.reloadGreen):
				self.reloadBars[N].setTexture(self.reloadGreen, 1)
				self.reloadBars[N].setTexOffset(self.modTS,
					.015, 0)
			# If the weapon isn't reloading, the reload bar is set to
			# green if it isn't already and the alpha texture is reset.
		
		return
# updateURHUD: updates all the HUD pieces in the upper right corner.

	def updateHUD(self, task):
		dt = globalClock.getDt()
		if (dt > .20):
			return task.cont
		# Find the amount of time that has passed since the last frame. If this amount is too large,
		# there's been a hiccup and this frame should be skipped.
		
		if(self.visible == True):
		# If the HUD isn't visible, there's no point in updating it.
			
			self.updateLLHUD()
			# Calls the updater method for the lower left corner of the HUD.
			
			#self.updateURHUD()
			# Calls the updater method for the upper right corner of the HUD.
			
			if(self.cycle.shutDown == True and 
				self.warningSeq.isPlaying() == False):
				self.warningSeq.loop()
		
			if(self.cycle.shutDown == False and
				self.warningSeq.isPlaying() == True):
				self.warningSeq.finish()
		
		return task.cont
# updateHUD: calls all of the other update methods every frame to keep the HUD
# up to date

	def hide(self):
		self.llFrame.hide()
		# Hides the lower left frame and all it's children.
		
		self.urFrame.hide()
		# Hides the upper right frame and all it's children.
		
		self.visible = False
		# Tells the HUD it's invisible.
		
		self.cycle = None
		
		return
# hide: Makes the HUD invisible.

	def show(self):
		self.llFrame.show()
		# shows the lower left frame and all it's children.
		
		self.urFrame.show()
		# shows the upper right frame and all it's children.

		self.visible = True
		# Tells the HUD it's visible.
		
		return
# show: Makes the HUD visible and start it updating.

	def showWarning(self):
		self.warning["text_fg"] = (1,1,1,1)
		return
# showWarning: sets the warning message alpha to 1.
	
	def fadeWarning(self, T):
		self.warning["text_fg"] = (1,1,1,T)
		return
# fadeWarning: sets the warning message text alpha based on input.	
