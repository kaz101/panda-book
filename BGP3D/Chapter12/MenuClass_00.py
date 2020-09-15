''' Menu Class
This class is designed to create a very
versatile, expandable menu structure.

The core concept of the class is to accept
lists of functions and lists of arguments
for them, so that it can use the methods
of other classes to complete the operations
it needs to.

The __init__ method and the initMenu 
method that takes the functions and
arguments have been seperated so that
the menu can be passed its own variables
and methods to use. This allows the menu
to pass itself as a parent menu if it 
creates a submenu. It also allows the 
menu to be passed its own kill method
so that it can remove itself.

The menu is designed so that it can be
manipulated by keyboard keys or by 
clicking the items with the mouse.

For this menu to work correctly, the 
functions it will call should be set up
to either take only a single argument, or
a single list of arguments, the way the menu's
__init__ and initMenu methods do.

Because the structure of the item, function, and argument lists can 
be confusing, here is an outline-style example of what it should like.

	List given to initMenu:
	   0: Type of menu
	   1: Title of menu
	   2: List of Menu Item Strings (the thing displayed)
	   3: List of functions for each item to execute if selected.
		  0: List of functions for item 0
		  1: List of functions for item 1
		  N: List of functions for item N
	   4: List of arguments for functions
		  0: List of Argument Lists for item 0
			 0: List of Arguments for function 0 of item 0
			 1: List of Arguments for function 1 of item 0
			 N: List of Arguments for function N of item 0
		  1: List of Argument Lists for item 1
			 0: List of Arguments for function 0 of item 1
			 1: List of Arguments for function 1 of item 1
			 N: List of Arguments for function N of item 1
		  N: List of Argument Lists for item N
			 0: List of Arguments for function 0 of item N
			 1: List of Arguments for function 1 of item N
			 N: List of Arguments for function N of item N 
'''

from direct.gui.DirectGui import *
from pandac.PandaModules import *

class Menu:
	def __init__(self, menuGraphics, fonts, inputManager = None):
		# The __init__ method takes a list of arguments
		# that need to be given in a particular order.
		
		self.menuGraphics = menuGraphics
		# The first argument is the model that contains
		# the geoms for the frames and buttons
		# that the menu can create. This model can be loaded 
		# from an egg created with egg-texture-cards.
		
		self.fonts = fonts
		# The second argument is a dictionary 
		# contains the fonts that will be used for the menu text.
		
		self.inputManager = inputManager
		# The third argument must be a class that accepts
		# keyboard input and has a keyMap full of True/False
		# values that indicate which keys are pressed, or a 
		# None-type object if keyboard control won't be used.
		
		self.self = self
		# Because menus are intended to be entirely self-contained,
		# no other part of the program will keep a reference to the 
		# menu. That means the menu is at risk of being garbage
		# collected when it shouldn't be. To prevent this, we'll have
		# the menu keep a reference of itself until it's ready to be
		# garbage collected.
		
	def initMenu(self, args):
		type = args[0]
		# The first argument in the list must be an indicator that
		# tells the menu what kind of menu it will be.
		
		if(args[1] != None):
			self.title = args[1]
		else:
			self.title = None
		# The second argument in the list must be a title text for
		# the menu, or a None-type object if the menu will have no
		# title.
		
		self.items = args[2]
		# The third argument in the list must be a list as well,
		# containing the strings that will become the text on the 
		# menu items.
		
		self.funcs = args[3]
		# The fourth argument in the list must be a list of the
		# functions that will be executed when the items are selected.
		# Each entry in this list is either a single function, or a 
		# list of functions, that will be executed when the item with
		# the same index is clicked or otherwise activated.
		
		self.funcArgs = args[4]
		# The fifth argument of the list must be a list of the arguments
		# that will be passed into the functions that are executed.
		
		self.buttons = []
		# This list will contain the DirectButtons that sit underneath
		# the DirectLabels to allow them to be clicked on.
		
		if(type == 0):
		# This checks if a particular type of menu will be created.
		
			self.frame = DirectFrame(
				geom = self.menuGraphics.find("**/Menu0"), relief = None,
				scale = (1.5,1,1.5), frameColor = (1,1,1,.75), 
				pos = (.2625,0,.43125), parent = base.a2dBottomLeft)
			# creates the frame that will act as a backdrop for the menu
			# using one of the texture cards in the menuGraphics.
			# Also scales, positions, and colors the menu frame. 
			# These numbers may need to be changed for other frame geometry.
			# Lastly, it sets base.a2dBottomLeft as the frame's parent, 
			# which adds the frame to the aspect2d scene graph and sticks
			# it to the bottom left corner of the screen.
			
			''' The two lines below are prep work for the following
			for loop and don't need to be repeated each iteration
			of the loop. '''
			framePadding = .1
			# framePadding is the amount of empty space above and 
			# below the buttons.
			
			height = self.frame.getHeight() - framePadding
			# Stores the height in a temporary variable to simplify
			# the calculations that use it.
			
			for N in range(len(self.items)):
			# Iterates through a series of integers that will
			# correspond to the indexes of self.items and
			# self.buttons.
		
				xPos = 0
				zPos = height/2 - (height / (len(self.items)-1)) * N
				# Calculates the position for item N on the menu
				# frame based on which number N is. This formula
				# will need to be adjusted based on the size and type
				# of the menu.
				
				self.buttons.append(DirectButton(
					command = self.activateItem, extraArgs = [N], 
					geom = (self.menuGraphics.find("**/BttnNormal"), 
							self.menuGraphics.find("**/BttnPushed"),
							self.menuGraphics.find("**/BttnNormal"),
							self.menuGraphics.find("**/BttnNormal")),
					relief = None, clickSound = None,
					rolloverSound = None, parent = self.frame,
					pos = (xPos, 0, zPos)))
				# Creates a DirectButton that uses the texture cards
				# in the menuGraphics model, has no sounds associated
				# with it, and is positioned according to the
				# calculations we just did.
				
				self.items[N] = DirectLabel(text = self.items[N], 
				text_font = self.fonts["silver"],
				text_fg = (1,1,1,.75), relief = None, 
				text_align = TextNode.ACenter, text_scale = .035,
				parent = self.buttons[N])
				# Creates a DirectLabel to replace the string in
				# the item list. This DirectLabel will appear on
				# top of the menu button. We use a DirectLabel instead
				# of the button text because it lets us use the height
				# of the DIrectLabel to center the text on the button.
				
				self.items[N].setPos(0,0,-self.items[N].getHeight()/2)
				# Uses the DirectLabel's height to vertically center the
				# text on the button.
		
		if(type == 3):
			self.frame = DirectFrame(
				geom = self.menuGraphics.find("**/Menu3"), 
				relief = None, scale = (1.5,1,1.5), 
				frameColor = (1,1,1,.75), parent = base.aspect2d)
			# creates the frame that will act as a backdrop for the menu
			# using one of the texture cards in the menuGraphics.
			# Also scales and colors the menu frame. 
			# These numbers may need to be changed for other frame geometry.
			# Lastly, it sets base.aspect2d as the frame's parent, 
			# which adds the frame to the aspect2d scene graph and sticks
			# it to the center of the screen.
			
			''' The two lines below are prep work for the following
			for loop and don't need to be repeated each iteration
			of the loop. '''
			framePadding = .1
			# framePadding is the amount of empty space above and 
			# below the buttons. It's also used for the amount of space
			# above the title.
			
			height = self.frame.getHeight()/2 - framePadding
			# Stores the height in a temporary variable to simplify
			# the calculations that use it. The height is divided by two
			# because the top half of the frame is dedicated to the title,
			# while the bottom half is used for the buttons.
			
			self.title = DirectLabel(text = self.title, 
				text_font = self.fonts["silver"], text_fg = (1,1,1,.75), 
				relief = None, text_align = TextNode.ACenter, 
				text_scale = .065, parent = self.frame, 
				pos = (0,0,height))
			# Creates a DirectLabel to act as the title of the menu. This
			# is filled with whatever text was given to the initMenu
			# method. It is made a child of the frame, and placed at the
			# top of the menu.
				
			for N in range(len(self.items)):
			# Iterates through a series of integers that will
			# correspond to the indexes of self.items and
			# self.buttons.
		
				xPos = 0
				zPos = -(height / (len(self.items)-1)) * N
				# Calculates the position for item N on the menu
				# frame based on which number N is. This formula
				# will need to be adjusted based on the size and type
				# of the menu. This calculation assumes that we're
				# only using the bottom half of the menu, which is why
				# it doesn't start with height/2 this time.
				
				self.buttons.append(DirectButton(
					command = self.activateItem, extraArgs = [N], 
					geom = (self.menuGraphics.find("**/BttnNormal"), 
							self.menuGraphics.find("**/BttnPushed"),
							self.menuGraphics.find("**/BttnNormal"),
							self.menuGraphics.find("**/BttnNormal")),
					relief = None, clickSound = None,
					rolloverSound = None, parent = self.frame,
					pos = (xPos, 0, zPos)))
				# Creates a DirectButton that uses the texture cards
				# in the menuGraphics model, has no sounds associated
				# with it, and is positioned according to the
				# calculations we just did.
				
				self.items[N] = DirectLabel(text = self.items[N], 
				text_font = self.fonts["silver"], 
				text_fg = (1,1,1,.75), relief = None, 
				text_align = TextNode.ACenter, text_scale = .035,
				parent = self.buttons[N])
				# Creates a DirectLabel to replace the string in
				# the item list. This DirectLabel will appear on
				# top of the menu button. We use a DirectLabel instead
				# of the button text because it lets us use the height
				# of the DIrectLabel to center the text on the button.
				
				self.items[N].setPos(0,0,-self.items[N].getHeight()/2)
				# Uses the DirectLabel's height to vertically center the
				# text on the button.
		
		if(self.inputManager != None):
		# checks if keyboard control is available before performing
		# keyboard-control-related actions.
			
			self.itemHL = 0
			# This holds the index of the menu item that is currently
			# highlighted.
			
			self.keyWait = 0
			# This variable counts the time between key-press-based
			# actions, to prevent too many from happening too quickly.
			
			self.highlightItem(0)
			# Highlights the first item on the menu.
		
			taskMgr.add(self.menuControl, "Menu Control")
			# Starts the task that allows the menu to be controlled
			# via the keyboard.
		
		return
# initMenu: Does the work of setting up the DirectGUI objects that the menu
# is made of, and also permanently stores the functions and function arguments
# the menu will need to perform it's duties. Lastly, it sets the first item in 
# the menu to be the default highlighted item and adds the task that allows 
# keyboard control, if an input manager was provided.

	def highlightItem(self, item):
		if(item < 0): item = len(self.items) - 1
		if(item == len(self.items)): item = 0
		# If the new item index number is out of bounds of the list, 
		# we change the item index to cause a wrapping effect. That way
		# if "up" is pressed when at the top of the menu, we highlight the
		# bottom, and vice versa.
		
		self.items[self.itemHL]["text_font"] = self.fonts["silver"]
		self.items[item]["text_font"] = self.fonts["orange"]
		self.itemHL = item
		# Changes the font of the old highlighted item back to silver, and
		# changes the font of the new highlighted item to orange. Also stores
		# the index number of the new highlighted item.
		
		return
# highlightItem: changes which DirectLabel is set to the highlight-type font
# to show the user what menu item will activate if they press "fire". Also
# updates the self.itemHL variable so the menu knows which item is highlighted.
	
	def activateItem(self, item):
		if(type(self.funcs[item]) == list):
		# Checks if the provided item was given a single function,
		# or a list of functions.
		
			for N in range(len(self.funcs[item])):
				if(self.funcArgs[item][N] != None):
					self.funcs[item][N](self.funcArgs[item][N])
				else:
					self.funcs[item][N]()
			# If there is a list of functions, this loop iterates through the
			# functions and calls each one with it's arguments, if it was given
			# any other than a None-type object.
			
		else:
			if(self.funcArgs[item] != None):
				self.funcs[item](self.funcArgs[item])
			else:
				self.funcs[item]()
			#If there was a single function, it's called with it's associated
			# arguments, unless the argument is just a None-type object.
			
		self.destroy()
		# The menu automatically removes itself once a choice has been made.
		
		return
# activateItem: executes all the stored functions that are associated with the
# item passed into this method. Once that's complete, the menu destroys itself.
		
	def menuControl(self, task):
		if(self.self == None):
			return task.done
		# If the menu has removed its reference to itself, then it is being deconstructed
		# and this task should be removed from the task manager, so that the task manager
		# won't keep a reference to this menu.
		
		dt = globalClock.getDt()
		if( dt > .20):
			return task.cont
		# Gets the amount of time that has passed since the last frame from the global clock.
		# If the value is too large, there has been a hiccup and the frame will be skipped.
			
		self.keyWait += dt
		# Increments the keyWait variable with the amount of time that passed
		# since last frame.
		
		if(self.keyWait > .25):
		# If enough time has passed since the last key press action
		# we can perform another.
			
			if(self.inputManager.keyMap["up"] == True):
				self.highlightItem(self.itemHL - 1)
				self.keyWait = 0
			# Highlights the next higher item in the menu.
			
			elif(self.inputManager.keyMap["down"] == True):
				self.highlightItem(self.itemHL + 1)
				self.keyWait = 0
			# Highlights the next lower item in the menu.
			
			elif(self.inputManager.keyMap["fire"] == True):
				self.activateItem(self.itemHL)
				self.keyWait = 0
			# Activates the highlighted menu item.
			
		return task.cont
# menuControl: Enables the menu to respond to keyboard events by monitoring
# the keyMap in the input manager.
		
	def destroy(self):
		for N in range(len(self.items)):
			self.items[0].destroy()
			self.buttons[0].destroy()
		if(self.title != None):
			self.title.destroy()
		self.frame.destroy()
		# Destroys all the DirectGui objects created by the menu.
		
		self.self = None
		# Removes the circular reference so it won't keep the menu
		# from being garbage collected anymore.
		
		return
# destroy: Does all the work of removing references to the menu to get
# it ready for garbage collection, except for ending the menuControl task.
# When that task detects that destroy has been called, it will remove itself.
		