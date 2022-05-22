import sys
import tkinter
from .ScrollableImage import ScrollableImage
from PIL import Image, ImageTk

class DisplayManager():
    def __init__(self, windowName):
        self.window = tkinter.Tk()
        self.window.geometry("1024x776")
        self.window.title = windowName

        self.rootPanel = tkinter.PanedWindow()
        self.rootPanel.config(width=200)
        self.rootPanel.pack(fill=tkinter.BOTH, expand=1)

        self.infoPanel = tkinter.PanedWindow(self.rootPanel, orient=tkinter.VERTICAL)
        self.rootPanel.add(self.infoPanel)

        self.provinceNameLabel = tkinter.Label(self.infoPanel, text="Hello World!")
        self.infoPanel.add(self.provinceNameLabel)

        self.mapDisplay = ScrollableImage(self.rootPanel, width=200, height=200)
        self.mapDisplay.pack()
        self.rootPanel.add(self.mapDisplay)

    def updateMapFromFile(self, file):
        self.mapDisplay.updateImage(ImageTk.PhotoImage(Image.open(file)))

    def startMainLoop(self):
	    self.window.mainloop()