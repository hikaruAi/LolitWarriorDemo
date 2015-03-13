from HPanda.HScene import HScene

##################
from panda3d.core import loadPrcFileData

####3
import StaticObjects

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
