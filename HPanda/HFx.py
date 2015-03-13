from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import NodePath, Vec3


class HExtendedParticles(ParticleEffect):
    count = 0

    def __init__(self, name0, config):
        # NodePath.__init__(self)
        ParticleEffect.__init__(self, name=name0 + str(HExtendedParticles.count))
        self.loadConfig(config)
        HExtendedParticles.count += 1

    def startInPos(self, pos, level, life=0):
        # self.reparentTo(scene.Base.render)
        #self.setPos(scene.Base.render,pos)
        ParticleEffect.start(self,parent=level.Base.render, renderParent=level.Base.render)
        self.setPos(pos)
        if life != 0:
            level.Base.taskMgr.doMethodLater(life, self.__cleanup, self.name + "+automaticCleanup")

    def startAttached(self, node, level, life,soft=True):
        ParticleEffect.start(self,parent=node, renderParent=level.Base.render)
        level.Base.taskMgr.doMethodLater(life, self.__cleanup, self.name + "-automaticCleanup",extraArgs=[soft])

    def start(self, parent, renderParent, level, life=0,soft=True):
        ParticleEffect.start(self, parent, renderParent)
        if life != 0:
            level.Base.taskMgr.doMethodLater(life, self.__cleanup, self.name + "+automaticCleanup",extraArgs=[soft])

    def __cleanup(self, t=None,soft=True):
        if soft:
            self.clearToInitial()
            self.disable()
        else:
            self.cleanup()
        #self.hide()
        #self.softStop()