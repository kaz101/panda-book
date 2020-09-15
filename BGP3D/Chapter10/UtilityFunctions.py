''' Utility Functions
This file doesn't contain a class. Instead it
contains some useful functions that different
parts of the game can take advantage of.
'''
import math, random

def trueDist(pos1, pos2):	
		return( math.sqrt( math.pow(pos2.getX() - pos1.getX(), 2) + math.pow(pos2.getY() - pos1.getY(), 2)) )
# trueDist: Simple function that takes two positions and 
# returns the distance between them, ignoring height.
		
def getRandom(val1, val2):
	if(val1 >= 0):
		rand = random.random() * (val2 - val1) + val1
	# If value 1 is non negative, generate a random number between value 1 and 2.
	else:
		rand = random.random()
		if(random.random() > .5):
			rand *= val1
		else: rand *= val2
	# If value 1 is negative, return a random number between value 1 and 2 using a method
	# that works for negatives.
	return(rand)
# getRandom: Returns a random number between the given values.