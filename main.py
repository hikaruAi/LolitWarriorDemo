from HPanda.HGame import HGame
from Scenes import Scene1

class MainGame (HGame):
    def __init__(self):
        HGame.__init__(self,title="Lolita Warrior -Demo-")
    def setup(self):
        self.currentScene=Scene1(self)

if __name__=="__main__":
    Game=MainGame()
    Game.run()