from HPanda.HGameObject import HDynamicObject
from panda3d.core import Point3, Vec3, NodePath
from math import sin
from random import random

class HFloatingObject(HDynamicObject):
    def __init__(self,name,scene,egg,x=0,y=0,z=0,direction=Vec3(0,0,1)):
        HDynamicObject.__init__(self,name,scene,egg,None,x,y,z)
        self.initPos=Point3(x,y,z)
        self.amplitud=0
        self.frecuency=0
        self.direction=direction
    def start(self,frequency=1,amplitud=2,randomOffset=True):
        self.frequency=frequency
        self.amplitud=amplitud
        if randomOffset:
            self.offset=random()
        else:
            self.offset=0
        self.scene.Base.taskMgr.add(self._floatTask,self.name+"_floatTask")
    def _floatTask(self,t):
        p=self.initPos+(self.direction*(sin((t.time+self.offset)*self.frequency)*self.amplitud))
        self.setPos(p)
        return t.cont

class HCilindricalBillboard(NodePath):
    def __init__(self,name,egg,level,x=0,y=0,z=0,directRender=True):
        self.name=name
        self.level=level
        NodePath.__init__(self,self.level.loadEgg(egg))
        if directRender:
            self.reparentTo(self.level.Base.render)
        self.setBillboardAxis()

class HFloatingCilindricalBillBoard(HFloatingObject):
    def __init__(self,name,egg,scene,x=0,y=0,z=0,direction=Vec3(0,0,1)):
        HFloatingObject.__init__(self,name,scene,egg,x,y,z,direction)
        self.setBillboardAxis()

class HOrbitingObject(NodePath):
    def __init__(self,name, level,egg,parent,radius,factor=0.01,direction=Vec3(1,0,0),randomStart=True):
        self.name=name
        self.level=level
        self.direction=direction
        self.radius=radius
        NodePath.__init__(self,name)
        self.reparentTo(parent)
        self.setPos(parent,0,0,0)
        self.orb=self.level.loadEgg(egg)
        self.orb.reparentTo(self)
        self.orb.setPos(self,direction*radius)
        self.factor=factor
        if randomStart:
            self.setHpr(direction*random()*360)
    def start(self):
        self.level.Base.taskMgr.add(self._orbit,self.name+"_orbitTask")
    def _orbit(self,t):
        if self.level.pause is False:
            self.setHpr(self,self.direction*self.factor*globalClock.getDt())
            #self.scene.drawLine(self.getPos(self.scene.Base.render),self.orb.getPos(self.scene.Base.render),autoClear=False)
        return t.cont