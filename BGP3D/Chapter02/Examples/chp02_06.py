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
		
w = World()
# Create an instance of the World class.

run()
# Begin the main loop the game will run on.