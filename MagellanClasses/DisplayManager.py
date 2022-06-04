import sys
import tkinter
from .ScrollableImage import ScrollableImage
from PIL import Image, ImageTk

class DisplayManager():
    def __init__(self, windowName):
        self.window = tkinter.Tk()
        self.window.geometry("1024x776")
        self.provinceNameText = tkinter.StringVar()
        self.provinceNameText.set("No Province Selected")
        self.provinceColorText = tkinter.StringVar()
        self.provinceColorText.set("Red: -- Green: -- Blue: --")
        self.window.title = windowName

        self.rootPanel = tkinter.PanedWindow()
        self.rootPanel.config(width=200)
        self.rootPanel.pack(fill=tkinter.BOTH, expand=1)

        self.infoPanel = tkinter.PanedWindow(self.rootPanel, width=250)
        provinceNameLabel = tkinter.Label(self.infoPanel, textvariable=self.provinceNameText)
        # provinceColorLabel = tkinter.Label(self.infoPanel, textvariable=self.provinceColorText)
        provinceNameLabel.pack(side=tkinter.LEFT)
        # provinceColorLabel.pack(side=tkinter.LEFT)
        self.infoPanel.add(provinceNameLabel)
        # self.infoPanel.add(provinceColorLabel)
        self.rootPanel.add(self.infoPanel)

        self.mapDisplay = ScrollableImage(self.rootPanel, width=200, height=200)
        self.mapDisplay.pack()
        self.rootPanel.add(self.mapDisplay)

    def updateMap(self, image):
        self.mapDisplay.updateImage(ImageTk.PhotoImage(image))

    def updateProvinceInfo(self, province):
        self.provinceNameText.set("Province: {}".format(province.name))
        self.provinceColorText.set("Red: {} Green: {} Blue: {}".format(province.color[0], province.color[1], province.color[2]))

    def startMainLoop(self):
	    self.window.mainloop()