# ##HPanda3D
# ##HGameObject

from direct.actor.Actor import Actor

from HUtils import *
from panda3d.bullet import BulletCharacterControllerNode, BulletRigidBodyNode, BulletGhostNode
from panda3d.bullet import BulletClosestHitSweepResult
from panda3d.core import TransformState, BitMask32, VBase3, Point3, Vec3, NodePath, LODNode

physicsTypes = {"static": 0, "character": 1, "dynamic": 2, "None": 3, "ghost": 4}


class HBulletRigidBodyNode(BulletRigidBodyNode):
    def __init__(self, name):
        BulletRigidBodyNode.__init__(self, name)
        self.customData = {"name": name}


class HNewGameObject(NodePath):
    def __init__(self, name, scene, visualMesh, physicsMesh=None, physicsType="character", shapeMargin=0.02, stepHeight=0.5, x=0, y=0, z=0, mass=0, convex=True,
                 directRender=True, parent=None):
        global physicsTypes
        self.name = name
        self.scene = scene
        NodePath.__init__(self, self.scene.loadEgg(visualMesh))
        if physicsMesh != None:
            if physicsType == "rigid":
                self.body = BulletRigidBodyNode(self.name + "_RigidBody")
                self.attachNewNode(self.body)
                m = self.scene.Base.loader.loadModel(physicsMesh)
                if convex:
                    sTuple = modelToConvex(m)
                else:
                    sTuple = modelToShape(m)
                sTuple[0].setMargin(shapeMargin)
                self.body.addShape(sTuple[0], sTuple[1])
                self.body.setMass(mass)
                self.body.setPythonTag("name", self.name + "_RigidBody")
                self.scene.world.attachRigidBody(self.body)
            elif physicsType=="character":
                m = self.scene.Base.loader.loadModel(physicsMesh)
                sTuple = modelToConvex(m)
                sTuple[0].setMargin(shapeMargin)
                self.body = BulletCharacterControllerNode(sTuple[0], stepHeight, self.name + "_Character")
                self.attachNewNode(self.body)
                self.body.setPythonTag("name", self.name + "_Character")
                self.scene.world.attachCharacter(self.body)

        self.setPos(x, y, z)
        if directRender:
            self.reparentTo(self.scene.Base.render)
        elif parent != None:
            self.reparentTo(parent)


class HGameObject():
    def __init__(self, name, scene, visualMeshEgg, parent, physicsType, physicsShapeEgg=None, shapeMargin=0.04,
                 animable=False, animationsDict=None, stepHeight=0.5, x=0, y=0, z=0, mass=0, perpixelShading=False):
        """

        :type name: str
        :type scene: HLevel
        :type visualMeshEgg: str
        :type parent: panda3d.core.NodePath
        :type physicsType: int
        :type physicsShapeEgg: str
        :type shapeMargin: float
        :type animable: bool
        :type animationsDict: dict
        :type stepHeight: float
        :type x: float
        :type y: float
        :type z: float
        :type mass: float
        :type perpixelShading: bool
        """
        self.name = name
        self.scene = scene
        if visualMeshEgg is not None:
            if animable:
                if animationsDict is not None:
                    self.vMesh = Actor(visualMeshEgg, animationsDict)
                    self.vMesh.setBlend(frameBlend=True)

                else:
                    self.vMesh = Actor(visualMeshEgg)
                    self.vMesh.setBlend(frameBlend=True)
            else:
                self.vMesh = scene.Base.loader.loadModel(visualMeshEgg)
        else:
            self.vMesh = None
        if physicsType == physicsTypes["character"]:
            print name + " is a character"
            self.shapeModel = self.scene.loadEgg(physicsShapeEgg)
            self.shape = modelToConvex(self.shapeModel)[0]
            self.shape.setMargin(shapeMargin)
            self.body = BulletCharacterControllerNode(self.shape, stepHeight, name)
            self.bodyNP = parent.attachNewNode(self.body)
            if visualMeshEgg is not None:
                self.vMesh.reparentTo(self.bodyNP)
            self.scene.world.attachCharacter(self.body)
            self.bodyNP.setPos(x, y, z)
            self.body.setPythonTag("name", name)
        elif physicsType == physicsTypes["dynamic"]:
            self.shapeModel = self.scene.loadEgg(physicsShapeEgg)
            self.shape = modelToConvex(self.shapeModel)[0]
            self.shape.setMargin(shapeMargin)
            self.body = BulletRigidBodyNode(name)
            self.body.setMass(mass)
            self.body.addShape(self.shape)
            self.bodyNP = parent.attachNewNode(self.body)
            if visualMeshEgg is not None:
                self.vMesh.reparentTo(self.bodyNP)
            self.scene.world.attachRigidBody(self.body)
            self.bodyNP.setPos(x, y, z)
            self.body.setPythonTag("name", name)
        elif physicsType == physicsTypes["ghost"]:
            self.shapeModel = self.scene.loadEgg(physicsShapeEgg)
            self.shape = modelToConvex(self.shapeModel)[0]
            self.shape.setMargin(shapeMargin)
            self.body = BulletGhostNode(name)
            # self.body.setMass(mass)
            self.body.addShape(self.shape)
            self.bodyNP = parent.attachNewNode(self.body)
            if visualMeshEgg is not None:
                self.vMesh.reparentTo(self.bodyNP)
            self.scene.world.attachGhost(self.body)
            self.bodyNP.setPos(x, y, z)
            self.body.setPythonTag("name", name)
        else:
            pass

            # ###3Events
            # self.scene.Base.taskMgr.add(self.onFrame,"onFrame")
        self.shaders = perpixelShading
        if self.vMesh is not None and not self.shaders:
            self.scene.Base.taskMgr.add(self.clearShaderTask, name + "_clearShader")
        # self.scene.Base.taskMgr.add(self._calcVel,self.name+"_calcVelTask")
        self._lastPos = Point3()
        self.velocity = Vec3()

    def _calcVel(self, t):
        if self.scene.pause is False:
            try:
                n = self.bodyNP.getPos()
                self.velocity = (n - self._lastPos) / globalClock.getDt()
                self._lastPos = n
            except:
                # print self.velocity
                pass
        return t.cont

    def clearShaderTask(self, t):
        self.vMesh.clearShader()
        print "Shader clear_", self.name

    def onFrame(self, task):
        pass

    def doRelativeSweepTest(self, relativePoint, BitMask=None, height=0.1):
        globalPoint = self.scene.Base.render.getRelativePoint(self.bodyNP, relativePoint)
        fromT = TransformState.makePos(self.bodyNP.getPos(self.scene.Base.render) + VBase3(0, 0, height))
        toT = TransformState.makePos(globalPoint + VBase3(0, 0, height))
        if BitMask != None:
            r = self.scene.world.sweepTestClosest(self.shape, fromT, toT, BitMask)
        else:
            r = self.scene.world.sweepTestClosest(self.shape, fromT, toT)
        if r.getNode() == self.body:
            return BulletClosestHitSweepResult.empty()
        else:
            return r

    def willCollide(self, relativePoint, bitMask=None, height=0.1):
        r = self.doRelativeSweepTest(relativePoint, bitMask, height)
        if r.getNode() == self.body:
            return False
        else:
            return r.hasHit()

    def doInverseRelativeSweepTest(self, relativePoint, bitMask=None, height=0.1):
        globalPoint = self.scene.Base.render.getRelativePoint(self.bodyNP, relativePoint)
        fromT = TransformState.makePos(self.bodyNP.getPos(self.scene.Base.render) + VBase3(0, 0, height))
        toT = TransformState.makePos(globalPoint + VBase3(0, 0, height))
        if bitMask != None:
            r = self.scene.world.sweepTestClosest(self.shape, toT, fromT, bitMask)
        else:
            r = self.scene.world.sweepTestClosest(self.shape, toT, fromT)
        if r.getNode() == self.body:
            return BulletClosestHitSweepResult.empty()
        else:
            return r

    def inverseWillCollide(self, relativePoint, bitMask=None, height=0.1):
        r = self.doRelativeSweepTest(relativePoint, bitMask, height)
        if r.getNode() == self:
            return False
        else:
            return r.hasHit()

    def destroy(self):
        if "Character" in str(self.body):
            self.scene.world.removeCharacter(self.body)
        elif "Rigid" in str(self.body):
            self.scene.world.removeRigidBody(self.body)
        elif "Ghost" in str(self.body):
            self.scene.world.removeGhost(self.body)
        self.bodyNP.removeNode()
        try:
            self.vMesh.removeNode()
        except:
            pass

    def isOnGround(self):
        r = self.willCollide(Point3(0, 0, -0.1), self.body.getIntoCollideMask(), 0)
        print r
        return r

    def setVelocity(self, v):
        globalV = self.scene.Base.render.getRelativeVector(self.bodyNP, v)
        self.body.setLinearVelocity(globalV)

    def applyForce(self, v):
        globalV = self.scene.Base.render.getRelativeVector(self.bodyNP, v)
        self.body.applyCentralForce(globalV)


class HInteractiveObject(HGameObject):
    def __init__(self, scene, name0, visualEgg, collisionEgg, mass, x0=0, y0=0, z0=0, margin=0.04,
                 sound=None, perpixelShading=True, CCD=False, CCDradius=0.05):
        HGameObject.__init__(self, name0, scene, visualEgg, scene.Base.render, 2, collisionEgg, margin, False, None,
                             0, x0, y0, z0, mass, perpixelShading)
        self.scene.Base.taskMgr.add(self.testCollision, self.name + "_testCollisionTask")
        if CCD:
            self.body.setCcdMotionThreshold(0.01)
            self.body.setCcdSweptSphereRadius(CCDradius)

    def onContact(self, bodyList):
        "Play sound"

    def testCollision(self, task):
        result = self.scene.world.contactTest(self.body)
        if result.getNumContacts() > 0:
            self.onContact(result)
        else:
            pass
        # if self.bodyNP.getZ(self.scene.Base.render)<50: self.destroy()
        return task.cont

    def destroy(self):
        self.scene.world.removeRigidBody(self.body)
        self.vMesh.removeNode()
        self.bodyNP.removeNode()
        self.scene.Base.taskMgr.remove(self.name + "_testCollisionTask")
        print self.name, "_destroyed"


class HDynamicObject(NodePath):
    def __init__(self, name, scene, visibleEgg, collisionEgg=None, x0=0, y0=0, z0=0, parent=None, margin=0.02, mass=0,
                 directRender=True, convex=True):
        self.name = name
        self.scene = scene
        NodePath.__init__(self, self.scene.loadEgg(visibleEgg))
        self.body = BulletRigidBodyNode(self.name + "_RigidBody")
        self.attachNewNode(self.body)
        if collisionEgg != None:
            m = self.scene.Base.loader.loadModel(collisionEgg)
            if convex:
                sTuple = modelToConvex(m)
            else:
                sTuple = modelToShape(m)
            sTuple[0].setMargin(margin)
            self.body.addShape(sTuple[0], sTuple[1])
            self.body.setMass(mass)
            self.body.setPythonTag("name", self.name + "_RigidBody")
            self.scene.world.attachRigidBody(self.body)
        self.setPos(x0, y0, z0)
        if directRender:
            self.reparentTo(self.scene.Base.render)
        elif parent != None:
            self.reparentTo(parent)

class HLodDynamicObject(NodePath):
    def __init__(self, name, scene, visibleLODsDict={"egg":("maxFar","minNear")}, collisionEgg=None, x0=0, y0=0, z0=0, parent=None, margin=0.02, mass=0,
                 directRender=True, convex=True):
        self.name = name
        self.scene = scene
        NodePath.__init__(self,LODNode(name+"_LODNode"))
        ###LOD###
        for k in visibleLODsDict.keys():
            v=base.loader.loadModel(k)
            v.reparentTo(self)
            self.node().addSwitch(visibleLODsDict[k][0],visibleLODsDict[k][1])
        #########
        self.body = BulletRigidBodyNode(self.name + "_RigidBody")
        self.attachNewNode(self.body)
        if collisionEgg != None:
            m = self.scene.Base.loader.loadModel(collisionEgg)
            if convex:
                sTuple = modelToConvex(m)
            else:
                sTuple = modelToShape(m)
            sTuple[0].setMargin(margin)
            self.body.addShape(sTuple[0], sTuple[1])
            self.body.setMass(mass)
            self.body.setPythonTag("name", self.name + "_RigidBody")
            self.scene.world.attachRigidBody(self.body)
        self.setPos(x0, y0, z0)
        if directRender:
            self.reparentTo(self.scene.Base.render)
        elif parent != None:
            self.reparentTo(parent)