from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, Filename, loadPrcFileData


class HGame(ShowBase):
    def __init__(self, sizeX=640, sizeY=480, title="Title", particles=True, fixedSize=True, cursorHide=False,
                 icon="None", cursorFile="None", posX=0, posY=0):
        """

        :param sizeX: Window horizontal size in pixels
        :param sizeY: Window vertical size i pixels
        :param title: Window's title bar text
        :param particles: Enable particles
        :param fixedSize: Window can be resized
        :param cursorHide: Hide cursor
        :param icon: filepath to window icon
        :param cursorFile: filepath to window cursor icon
        :param posX: window initial X position
        :param posY: window initial Y position
        """
        ShowBase.__init__(self)
        if particles:
            base.enableParticles()
        self.propierties = WindowProperties()
        loadPrcFileData("", "win-size " + str(sizeX) + " " + str(sizeY))
        loadPrcFileData("", "window-title " + title)
        self.propierties.setFixedSize(fixedSize)
        self.propierties.setCursorHidden(cursorHide)
        if icon != "None":
            self.propierties.setIconFilename(Filename(icon))
        if cursorFile != "None":
            self.propierties.setCursorFilename(Filename(cursorFile))
        if posX != 0 and posY != 0:
            self.propierties.setOrigin(posX, posY)
        base.win.requestProperties(self.propierties)
        self.setup()

    def setup(self):
        pass
