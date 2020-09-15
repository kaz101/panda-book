''' InputManager Class
The purpose of this class is to have an object
that will record user input and retain that 
information for use by other classes.
'''

from direct.showbase.DirectObject import DirectObject

class InputManager(DirectObject):
	def __init__(self):
		self.keyMap = {"w" : False,
						"s" : False,
						"a" : False,
						"d" : False,
						"mouse1" : False,
						"mouse3" : False}
		# Creates a key map to store the state of relevant keyboard keys.
						
		self.accept("w", self.setKey, ["w", True])
		self.accept("s", self.setKey, ["s", True])
		self.accept("a", self.setKey, ["a", True])
		self.accept("d", self.setKey, ["d", True])
		self.accept("mouse1", self.setKey, ["mouse1", True])
		self.accept("mouse3", self.setKey, ["mouse3", True])
		# Registers the events for key and mouse presses and 
		# connects them to the setKey method.
		
		self.accept("w-up", self.setKey, ["w", False])
		self.accept("s-up", self.setKey, ["s", False])
		self.accept("a-up", self.setKey, ["a", False])
		self.accept("d-up", self.setKey, ["d", False])
		self.accept("mouse1-up", self.setKey, ["mouse1", False])
		self.accept("mouse3-up", self.setKey, ["mouse3", False])
		# Registers the events for key and mouse releases and 
		# connects them to the setKey method.
		
	def setKey(self, key, value):
		self.keyMap[key] = value
		return
# setKey: stores the given value in the given key within the key map dictionary.