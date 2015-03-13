from panda3d.core import VBase4, DirectionalLight, AmbientLight, NodePath

class HSunLamp(NodePath):
    def __init__(self,name,level,rx=0,ry=0,rz=0,x=0,y=0,z=0,color=(1,1,1,1),affectAll=True,showFrustum=False):
        self.name=name
        self.level=level
        self.lamp=DirectionalLight(name)
        NodePath.__init__(self,self.lamp)
        #self.attachNewNode(self.lamp)
        self.lamp.setColor(VBase4(color[0],color[1],color[2],color[3]))
        if affectAll:
            self.level.Base.render.setLight(self)
            self.reparentTo(self.level.Base.render)
        self.setPos(x,y,z)
        if showFrustum:
            self.lamp.showFrustum( )
        self.setRotation(rx,ry,rz)

    def setRotation(self,x,y,z):
        pass
        p=270-x
        h=x
        r=y
        #self.setHpr()

class HAmbientLight(NodePath):
    def __init__(self,name,level,color=(1,1,1,1),affectAll=True):
        self.name=name
        self.level=level
        self.lamp=AmbientLight(name)
        NodePath.__init__(self,self.lamp)
        #self.attachNewNode(self.lamp)
        self.lamp.setColor(VBase4(color[0],color[1],color[2],color[3]))
        if affectAll:
            self.level.Base.render.setLight(self)
            self.reparentTo(self.level.Base.render)
