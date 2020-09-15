''' InputManager Class
The purpose of this class is to have an object
that will record user input and retain that 
information for use by other classes.
'''

from direct.showbase.DirectObject import DirectObject

class InputManager(DirectObject):
	def __init__(self):
		self.keyMap = {"up" : False,
						"down" : False,
						"left" : False,
						"right" : False,
						"fire" : False,
						"mouse1" : False,
						"mouse3" : False}
		# Creates a key map to store the state of relevant keyboard keys.
						
		self.accept("w", self.setKey, ["up", True])
		self.accept("s", self.setKey, ["down", True])
		self.accept("a", self.setKey, ["left", True])
		self.accept("d", self.setKey, ["right", True])
		self.accept("enter", self.setKey, ["fire", True])
		self.accept("mouse1", self.setKey, ["mouse1", True])
		self.accept("mouse3", self.setKey, ["mouse3", True])
		# Registers the events for key and mouse presses and 
		# connects them to the setKey method.
		
		self.accept("w-up", self.setKey, ["up", False])
		self.accept("s-up", self.setKey, ["down", False])
		self.accept("a-up", self.setKey, ["left", False])
		self.accept("d-up", self.setKey, ["right", False])
		self.accept("enter-up", self.setKey, ["fire", False])
		self.accept("mouse1-up", self.setKey, ["mouse1", False])
		self.accept("mouse3-up", self.setKey, ["mouse3", False])
		# Registers the events for key and mouse releases and 
		# connects them to the setKey method.
		
	def setKey(self, key, value):
		self.keyMap[key] = value
		return
# setKey: stores the given value in the given key within the key map dictionary.