from panda3d.core import Vec3,Point3,NodePath

class BaseCamera():
    def __init__(self,scene):
        self.scene=scene
        base.disableMouse()
        self.scene.Base.taskMgr.add(self.execute,"CameraAI",priority=128)

    def execute(self,t):
        pass

class ThirdPersonCamera(BaseCamera):
    def __init__(self,scene,target,lookAtHeight,initX=0,initY=0,initZ=0,speed=1,debug=False):
        BaseCamera.__init__(self,scene)
        self.target=target
        self.lookAtTarget=self.scene.loadEgg("HPanda/axis")
        self.lookAtTarget.setScale(1)
        self.lookAtTarget.setZ(self.target,lookAtHeight)
        self.lookAtTarget.reparentTo(target)
        #self.lookAtTarget.setScale(1)
        self.scene.camera.setPos(self.scene.render,initX,initY,initZ)
        self.scene.camera.lookAt(self.lookAtTarget)
        self.positionTarget=self.scene.loadEgg("HPanda/axis")
        self.positionTarget.setPos(self.scene.render,initX,initY,initZ)
        self.positionTarget.reparentTo(self.target)
        self.speed=speed
        if debug is False:
            self.lookAtTarget.hide()
            self.positionTarget.hide()

    def execute(self,t):
        v = self.positionTarget.getPos( self.scene.camera )
        if v.almostEqual(Vec3(0,0,0),0.01):
            return t.cont
        else:
            self.scene.camera.setPos( self.scene.camera , v*globalClock.getDt()*self.speed )
            self.scene.camera.lookAt( self.lookAtTarget )
        return t.cont


class HMouseLook():
    def __init__(self, showBase, xFact=500, yFact=500, applyH=True, applyP=True):
        self.Base = showBase
        self.xFact = xFact
        self.yFact = yFact
        self.centerMouse()
        self.setTask()
        self.centerX = base.win.getXSize() / 2
        self.centerY = base.win.getXSize() / 2
        self.dH = 0
        self.dP = 0
        self.applyH = applyH
        self.applyP = applyP
        self.hideMouse()

    def hideMouse(self, value=True):
        prop = WindowProperties()
        prop.setCursorHidden(value)
        base.win.requestProperties(prop)

    def disable(self):
        self.Base.removeTask("updateTask")

    def enable(self):
        self.setTask()

    def setTask(self):
        # if base.mouseWatcherNode.hasMouse():
        self.Base.addTask(self.updateTask, "updateTask")
        print "Task Added"

    def updateTask(self, task):
        try:
            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()
        except:
            self.centerMouse()
            return task.cont
        if x == 0:
            self.dH = 0
        if y == 0:
            self.dP = 0
            self.centerMouse()
        if x == 0 and y == 0:
            return task.cont
        else:
            dt = globalClock.getDt()
            self.dH = -x * self.xFact * dt
            self.dP = y * self.xFact * dt
            if self.applyH:
                self.Base.camera.setH(self.Base.camera, self.dH)
            if self.applyP:
                self.Base.camera.setP(self.Base.camera, self.dP)
            self.Base.camera.setR(self.Base.render, 0)
            self.centerMouse()
            return task.cont

    def centerMouse(self):
        base.win.movePointer(0, base.win.getXSize() / 2, base.win.getYSize() / 2)