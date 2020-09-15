from direct.gui.DirectGui import *
from pandac.PandaModules import *

class HUD:
	def __init__(self, fonts):
		self.modTS = TextureStage("Modulate")
		self.modTS.setMode(TextureStage.MModulate)
		# Creats a texture stage to use for making alpha cut outs.
		
		self.createLLHUD(fonts)
		# Creates the lower left corner of the HUD.
		
		self.visible = False
		# a boolean variable that let's the HUD know if it is visible
		# or not.
		
		taskMgr.add(self.updateHUD, "Update HUD")
		# Adds the task that keeps HUD info up to date.
		
	def setCycle(self, cycle):
		self.cycle = cycle
		return
#setCycle: sets the cycle that the HUD will report on.
			
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
		# Loads and alpha texture to use as a cut out for the
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
		
		return task.cont
#updateHUD: calls all of the other update methods every frame to keep the HUD
# up to date

	def hide(self):
		self.llFrame.hide()
		# Hides the lower left frame and all it's children.
		
		self.visible = False
		# Tells the HUD it's invisible.
		
		return
#hide: Makes the HUD invisible.

	def show(self):
		self.llFrame.show()
		# shows the lower left frame and all it's children.

		self.visible = True
		# Tells the HUD it's visible.
		
		return
#show: Makes the HUD visible and start it updating.
