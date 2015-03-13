from direct.actor.Actor import Actor
from panda3d.bullet import BulletCharacterControllerNode as Character
from panda3d.core import NodePath
from HUtils import *


class HPlayer(NodePath): ###Implementarlo como Nodepath y el actor como hijo
    def __init__(self, name, scene, visualMesh, collisionMesh, animations, step=0.2, margin=0.01):
        """
        :type collisionMesh: String
        :type visualMesh: String
        :type name: String
        :type margin: Float
        :param name: Name
        :param scene: Scene
        :param visualMesh: Egg to use as visual mesh
        :param collisionMesh: Egg to use as convex shape for physics
        :param animations: Animation dict
        :param step: Character step height
        :param margin: Physics shape margin
        """
        self.name = name
        self.scene = scene
        m = self.scene.Base.loader.loadModel(collisionMesh)
        sTuple = modelToConvex(m)
        sTuple[0].setMargin(margin)
        self.body = Character(sTuple[0], step, self.name + "_Character")
        #self.attachNewNode(self.body)
        self.body.setPythonTag("name", self.name + "_Character")
        self.scene.world.attachCharacter(self.body)

        NodePath.__init__(self,self.body)
        self.actor=Actor(self.scene.loadEgg(visualMesh), animations)
        self.actor.reparentTo(self)
        #self.setPhysics(collisionMesh, step, margin)

    def setPhysics(self, collisionMesh, step, margin):
        m = self.scene.Base.loader.loadModel(collisionMesh)
        sTuple = modelToConvex(m)
        sTuple[0].setMargin(margin)
        self.body = Character(sTuple[0], step, self.name + "_Character")
        self.attachNewNode(self.body)
        self.body.setPythonTag("name", self.name + "_Character")
        self.scene.world.attachCharacter(self.body)
        self.actor.reparentTo(self)
