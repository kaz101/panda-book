from direct.showbase.ShowBase import ShowBase

class World(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        #ShowBase.setBagroundColor(0,0,200)
        self.track = loader.loadModel('/home/kaz/Downloads/BGP3D/Models/Track.egg')
        self.track.reparentTo(render)

w = World()

#base = ShowBase()
w.run()
