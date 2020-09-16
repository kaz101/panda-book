from direct.showbase.ShowBase import ShowBase
from direct.task import Task

class World(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.track = loader.loadModel('BGP3D/Models/Track.egg')
        self.track.reparentTo(render)
        self.camera.setZ(10)
        self.accept('w-down',self.moveForward)
        #taskMgr.add(self.moveForward, 'moveForward')

    def moveForward(self):
        self.camera.setY(self.camera.getY() + 1)
        print('keyPressed')
    def moveLeft(self):
        self.camera.setX(self.camera.getX() - 1)
        print('keyPressed')
    def moveRight(self):
        self.camera.setX(self.camera.getX() + 1)
        print('keyPressed')
    def moveBack(self):
        self.camera.setY(self.camera.getY() - 1)
        print('keyPressed')
w = World()
w.disableMouse()

w.setBackgroundColor(0,0,200)

w.accept('w',w.moveForward)
w.accept('a',w.moveLeft)
w.accept('s',w.moveBack)
w.accept('d',w.moveRight)

#base = ShowBase()
w.run()
