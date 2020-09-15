import direct.directbase.DirectStart
# Import the fundamental components of Panda3D.

class World:
# Create a new class called World

	def __init__(self):
	# Define a method that will be run when an instance of World is created.
	
		base.setBackgroundColor(0, 0, 0)
		# Change the background of the default window to black.
		
		self.track = loader.loadModel("../Models/Track.egg")
		self.track.reparentTo(render)
		# Load the track model and add it to the scene graph as a child of render.
		
		self.track.setPos(0,0,-5)
		# Move the track down 5 units on the Z axis.
		
		self.cycle1 = loader.loadModel("../Models/Cycle.bam")
		self.cycle1.reparentTo(render)
		self.cycle1.setPos(2,15,0)
		self.cycle2 = loader.loadModel("../Models/Cycle.bam")
		self.cycle2.reparentTo(render)
		self.cycle2.setPos(-2,15,0)
		# Load two cycle models, add them to scene graph as children of render,
		# and reposition them.
		
		self.cycle2.setRenderModeWireframe()
		# Changes the wireframe mode render attribute of the cycle2 NodePath
		# to turn wireframe mode on.
		
w = World()
# Create an instance of the World class.

run()
# Begin the main loop the game will run on.