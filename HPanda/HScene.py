# ##HPanda Library
# Level related classes

# ###CopyRightNotice####

# ######################

# ###IMPORTS####
from math import sin

from HUtils import *
from panda3d.core import Vec3, LineSegs, NodePath
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletDebugNode, BulletRigidBodyNode
from direct.gui.OnscreenText import OnscreenText
# from panda3d.core.TextProperties import TextProperties


class HScene():
    def __init__(self, showbase, physicsDebug=True,name="Scene"):
        """


        :type self.Base: direct.showbase.ShowBase.ShowBase
        :type showbase: direct.showbase.ShowBase.ShowBase
        :type physicsDebug: bool
        """
        print "Creating scene"
        self.name=name
        self.Base = showbase
        self.render=self.Base.render
        self.camera=self.Base.cam
        self.debugDrawing = physicsDebug
        self.pause = False
        self.bulletSubstep = 0.008
        self.activeLog=False

    def loadAssets(self):
        print "Loading Assets"

    def renderAssets(self):
        print "Rendering assets"

    def setCamera(self):
        print "Setting camera"

    def setLights(self):
        print "Setting lights"

    def destroy(self):
        print "Destroying scene"

    def loadEgg(self, egg):
        """
        :type egg: str
        :rtype : panda3d.core.NodePath
        """
        return self.Base.loader.loadModel(egg)

    def renderModel(self, model):
        """

        :type model: str
        """
        model.reparentTo(self.Base.render)

    def renderEgg(self, egg):
        """

        :type egg: str
        :return pada3d.core.NodePath
        """
        m = self.loadEgg(egg)
        self.renderModel(m)
        return m

    def setPhysics(self):
        print "Setting physics"
        self.world = BulletWorld()
        self.world.setGravity(Vec3(0, 0, -10))
        self.Base.taskMgr.add(self.physicsUpdate, "physicsUpdate", priority=0)
        if self.debugDrawing:
            print "Debug drawing"
            self.debug = BulletDebugNode("debug")
            self.debug.showWireframe(True)
            self.debug.showBoundingBoxes(False)
            self.debug.showNormals(True)
            self.debugNP = self.Base.render.attachNewNode(self.debug)
            self.debugNP.show()
            self.world.setDebugNode(self.debug)

    def physicsUpdate(self, task):
        if not self.pause:
            dt = globalClock.getDt()
            self.world.doPhysics(dt, 2, self.bulletSubstep)  # #0.009-0.008
            # print "Physics step"
        return task.cont

    def cameraShake(self, amplitud=0.01, frecuencia=5):
        """

        :type amplitud: float
        :type frecuencia: float
        """
        self.Base.camera.setZ(self.Base.camera, sin(globalClock.getRealTime() * frecuencia) * amplitud)

    def eggToStatic(self, egg, parent, margin=0.01, name="static"):
        """

        :type egg: str
        :type parent: panda3d.core.NodePath
        :type margin: float
        :type name: str
        :return: tuple(pada3d.bullet.BulletRigidBodyNode,panda3d.core.NodePath)
        """
        m = self.Base.loader.loadModel(egg)
        sTuple = modelToShape(m)
        sTuple[0].setMargin(margin)
        static = BulletRigidBodyNode(name)  # H
        static.addShape(sTuple[0], sTuple[1])
        np = parent.attachNewNode(egg)
        self.world.attachRigidBody(static)
        return static, np

    def togglePause(self):
        """

        """
        if self.pause:
            self.pause = False
        else:
            self.pause = True
        print "Toggle pause", self.pause

    def activateLog(self):
        self.activeLog=True
        self.logText = OnscreenText("NO LOG", scale=0.07, fg=(1, 0, 0, 0.8), bg=(0, 0, 1, 0.2), frame=(0, 1, 0, 0.2),
                                    pos=(-1.05, .9), mayChange=True, align=0)
        self.__logTextLenght = 0
        self.__logAbsoluteLenght = 0
        self.__logText = ""
        self.logText.reparentTo(self.Base.aspect2d)

    def log(self, *args):
        if self.activeLog is False:
            return None
        s = str(self.__logAbsoluteLenght) + ":"
        for a in args:
            s += str(a) + " "
        if self.__logTextLenght < 10:
            self.logText.appendText("\n" + s)
        else:
            self.__logTextLenght = 0
            self.logText.clearText()
            self.logText.setText(s)
        self.__logTextLenght += 1
        self.__logAbsoluteLenght += 1
        self.__logText.join(s)
    def loadFont(self,string):
        return self.Base.loader.loadFont(string)
    def drawLine(self,fromP,toP,thickness=2,color=(1,0,0,1),autoClear=True):
        if autoClear:
            try:
                self.debugLineNP.removeNode()
            except:
                pass
        self.debugLine=LineSegs("DebugLine")
        self.debugLine.reset()
        self.debugLine.setThickness(thickness)
        self.debugLine.setColor(color)
        self.debugLine.moveTo(fromP)
        self.debugLine.drawTo(toP)
        self.debugLineNode=self.debugLine.create()
        self.debugLineNP=NodePath(self.debugLineNode)
        self.debugLineNP.reparentTo(self.Base.render)
        return self.debugLineNP