from logging import root
import sys
import tkinter
from tkinter import filedialog
from .ScrollableImage import ScrollableImage
from PIL import Image, ImageTk

def doNothing(*argv):
    pass # Why are you looking here? What do you expect?

class DisplayManager():
    def __init__(self, mapModes):
        
        self.window = tkinter.Tk()
        self.window.geometry("1024x776")
        self.window.title("Magellan EU4") # TODO: Change title with mod folder name?

        self.provinceNameText = tkinter.StringVar()
        self.provinceNameText.set("No Province Selected")
        self.provinceColorText = tkinter.StringVar()
        self.provinceColorText.set("Red: -- Green: -- Blue: --")

        # The following must be populated
        self.onMenuFileOpen = doNothing
        self.onNewMapMode = doNothing

        menubar = tkinter.Menu(self.window)

        fileMenu = tkinter.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open", command=(lambda : self.onMenuFileOpen(filedialog.askdirectory())))
        fileMenu.add_command(label="Save", command=doNothing)
        menubar.add_cascade(label="File", menu=fileMenu)

        mapModeMenu = tkinter.Menu(menubar, tearoff=0)
        for mapMode in mapModes:
            mapModeMenu.add_command(label=mapMode.getName(), command=(lambda : self.onNewMapMode(mapMode)))
        menubar.add_cascade(label="Mapmode", menu=mapModeMenu)

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

        self.window.config(menu=menubar)
        self.rootPanel.add(self.mapDisplay)

    def updateMap(self, image):
        self.mapDisplay.updateImage(ImageTk.PhotoImage(image))

    def updateProvinceInfo(self, province):
        self.provinceNameText.set("Province: {}".format(province.name))
        self.provinceColorText.set("Red: {} Green: {} Blue: {}".format(province.color[0], province.color[1], province.color[2]))

    def startMainLoop(self):
        self.window.mainloop()