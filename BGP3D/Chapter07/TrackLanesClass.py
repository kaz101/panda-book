''' TrackLanes Class
This class creates and owns the markers that populate the
track and are used by many things in the game to understand
the shape and position of parts of the track.
'''

from pandac.PandaModules import EggData, Point3

from MarkerClass import Marker
from UtilityFunctions import trueDist

class TrackLanes:
	def __init__(self):
		MarkerEgg = EggData()
		# Creates a new, but temporary, EggData object, which is the object used to store raw, unprocessed eggs.
			
		MarkerEgg.read("../Models/Markers.egg")
		# Instructs the EggData object to read in an egg file.
		# This loads the lines and vertices that make up the AI Path.
		
		self.markerRoot = render.attachNewNode("MarkerRoot")
		# Creates a node to serve as a parent to all the markers, for ease of clean up.
		
		markers = self.createMarkers(MarkerEgg)
		self.prepMarkers(markers)
		# Fills the marker list with markers according to the MarkerEgg and then breaks them down into lanes.
		
		for L in self.lanes:
			for M in L:
				M.setFacing()
		# Sets each marker to lookAt it's nextMarker.
	
	def createMarkers(self, eggData):
		
		markers = []
		# creates a temporary list to store the markers until they are broken up into lanes.
	
		vertexPool = eggData.getFirstChild()		
		# Gets the vertex pool from the egg file. The egg is modified so the vertex pool is always first.
	
		count = 0
		# Initializes a count variable that will be used to walk through the vertices in the pool.
		
		while (count != -1):
		# This while loop does the work of pulling the vertices from the pool and creating Markers with their position data.
		# The condition used is -1 so that the loop won't quit until it is told to. When the getVertex call fails to get a vertex
		# the count will be set to -1 to end the loop.
	
			vertex = vertexPool.getVertex(count)
			# Gets the vertex with the index equal to what the count is at.
		
			if (vertex != None):
			# Verifies that getVertex actually got a vertex from the pool
		
				if (vertex.getNumDimensions() == 3):
				# Checks to make sure the vertex has 3 dimensions. This check must be done before using vertex.getPos3()
				# to prevent an error.
					
					vertexPos = Point3(vertex.getPos3().getX(), vertex.getPos3().getZ() * -1, vertex.getPos3().getY())
					
					markers.append(Marker(vertexPos))
					# Creates a new marker with the position of the vertex and appends it to the markers list.
					
				count += 1
				# Increments the count
			
			else: count = -1
			# If the getVertex call failed to pull a vertex from the pool we set the count to -1 in order to end the while loop.
		
		switch = False	
		# This switch is used to fulfill the necessary condition of the while loop.
		
		while (switch == False):
		# This loop will walk through the children of the egg file. We already got the vertex pool earlier so we know the next child 
		# will be a line. We can use getNextChild() because getFirstChild() has already been called on the
		# egg. This loop doesn't require a count, so we use a simple switch to run the loop until all the lines have been processed.
		
			child = eggData.getNextChild()
			# Gets the first (or next) line from the egg.
			
			if (child != None):
			# Verifies that getNextChild actually got something from the egg.
			
				if (str(child.getClassType()) == "EggLine"):
				# If so, Verifies that the child we got is a line.
				
					vertA = child.getVertex(0).getIndex()
					vertB = child.getVertex(1).getIndex()
					# Gets the indexes of the two verticies the line references. Since it is a line, it will always reference
					# exactly 2 verticies. The indexes of these vertices will be the same as the indexes of their corresponding
					# markers in the marker list because the marker list was generated by walking through the vertices.
					
					markers[vertA].adjMarkers.append(markers[vertB])
					markers[vertB].adjMarkers.append(markers[vertA])
					# Adds the index of each vertex (same as the marker indexes) to the other marker's list of adjacent markers
					# so they will know they are adjacent to one another.
			
			else:
				switch = True
			# If the no more children exist in the egg file then we've finished processing lines and we can exit the loop.
		return(markers)
# createMarkers: Takes the raw egg data from the egg file and uses it to create the markers
# at their appropriate positions.
		
	def prepMarkers(self, markers):
		self.lanes = []
		# Creates a list to store the finished marker lanes.
		
		for M in markers:
			if(M.getPos().getY() == 0 and len(M.adjMarkers) < 2):
				self.lanes.append([M])
		# Finds the start markers for each lane. These markers always have y = 0 and only one adjacent Marker.
		
		for L in self.lanes:			
			processed = [] # A list to hold indexes for markers already processed in the next loop.
			L[0].nextMarker = L[0].adjMarkers[0]
			L[0].adjMarkers[0].prevMarker = L[0]
			# Sets the start marker's next marker as the index of the only one adjacent to it. The start and finish markers are 
			# the only ones with a single adjacent marker.
			
			L[0].lane = self.lanes.index(L)
			L[0].index = 0
			# Tells the marker it what lane it's in and that it has an index of 0 in the list.
			
			processed.append(L[0])
			# adds the start marker's index to the processed list.
			
			M = L[0].nextMarker
			# sets the start marker's next marker as M.
			
			while M != None:
			# M will be set to none when the last marker in the chain is reached.
			
				if(len(M.adjMarkers) > 1):
				# Checks if M is adjacent to more than one other marker. If so, we need to determine which one is
				# the next marker in the chain.
					
					if(M.adjMarkers[0] in processed):
					# Checks if the first marker in M's adjacent marker lists has been processed. 
						
						M.nextMarker = M.adjMarkers[1]
						M.adjMarkers[1].prevMarker = M
						# If so, that means the second marker in M's adjacent marker list is the next in the chain.
						
					else:
						M.nextMarker = M.adjMarkers[0]
						M.adjMarkers[0].prevMarker = M
					# If not, then the first marker in M's adjacent marker list is the next in the chain.
					
					processed.append(M)
					# Adds M to the processed list.
					
					M.lane = self.lanes.index(L)
					M.index = len(L)
					L.append(M)
					# Tells the marker it's lane and it's index in the list and then adds it to the list.
					
					M = M.nextMarker
					# Makes the old M's next marker the new M.
				else:
					M.index = len(L)
					L.append(M)
					# Tells the marker it's index in the list and then adds it to the list.
					
					M.nextMarker = L[0]
					L[0].prevMarker = M
					# If M only has one adjacent marker, it is the end of the chain. That means it's next marker should be the start marker.
					
					M = None
					# sets M to None to end the loop.
					
		for M in markers:
			M.adjMarkers = None
			M.np.reparentTo(self.markerRoot)
		# clears out the adjacent markers variable in each marker. Now that we have the next marker for each of them, we don't need
		# to know what's adjacent anymore.
		
		return
# prepMarkers: Organizes the markers into groups based on their connections and order. The data in the 
# egg file describes two lanes on the track, and each lane is placed into its own group.

	def getNearestMarker(self, cycle):
		marker = self.lanes[0][0]
		# assumes that the first marker in lane 0 is the closest, to start with.
		for L in self.lanes:
			for M in L:
				if(trueDist(cycle.getPos(), M.getPos()) < trueDist(cycle.getPos(), marker.getPos())):
					marker = M
				# Iterates through all the markers on the track, always choosing the closest marker
				# from each comparison to check in future iterations.
		return(marker)
# getNearestMarker: Returns the marker that is closest to the provided cycle.