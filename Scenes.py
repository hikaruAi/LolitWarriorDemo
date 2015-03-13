from HPanda.HScene import HScene

##################
from panda3d.core import loadPrcFileData, TextureStage

####3
import Scene_01_static_objects

assets="3d/"
windowTitle = "LolitaWarrior -DEMO-"
windowX = 640
windowY = 480
perpixelShading = False
showFPS = True
debugPhysics = False
debugView = False
debugLights = False
pauseKey = "p"
filters = False
bulletSteps = 10
pystats=False

# ####Preferences#####
loadPrcFileData("", "win-size " + str(windowX) + " " + str(windowY))
loadPrcFileData("", "window-title " + windowTitle)
loadPrcFileData("", "allow-incomplete-render 1")
# loadPrcFileData("", "bullet-solver-iterations " + str(bulletSteps))
if showFPS:
    loadPrcFileData("", "show-frame-rate-meter #t")
if pystats:
    loadPrcFileData("","want-pstats 1")
    loadPrcFileData("", "task-timer-verbose 1")
    loadPrcFileData("","pstats-tasks 1")

#####################

class Scene1(HScene):
    def __init__(self,base):
        HScene.__init__(self,base)
        self.debugDrawing=debugPhysics
        self.setPhysics()
        self.setStatics()
        self.setCamera()
        self.n=0
        self.Base.taskMgr.add(self._loop,"Scene1_loop")
    def _loop(self,t):
        ta=t.time*0.2
        self.lake_01.setTexOffset(TextureStage.getDefault(), ta/2,ta)
        self.lake_02.setTexOffset(TextureStage.getDefault(), ta/2,ta)
        self.lake_03.setTexOffset(TextureStage.getDefault(), ta/2,ta)
        self.lake_04.setTexOffset(TextureStage.getDefault(), ta/2,ta)
        #print self.n
        return t.cont
    def setCamera(self):
        self.Base.camLens.setNearFar(1, 110)
    def setStatics(self):
        Scene_01_static_objects.setup(self)

