from logging import root
import sys
import tkinter
#from ttk import 
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import HORIZONTAL, RAISED, VERTICAL, filedialog, ttk
from .ScrollableImage import ScrollableImage
from PIL import ImageTk

def doNothing(*argv):
    pass # Why are you looking here? What do you expect?

class DisplayManager():
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.geometry("1024x776")
        self.window.title("Magellan EU4") # TODO: Change title with mod folder name?

        # The following must be populated
        self.onMenuFileOpen = doNothing
        self.onNewMapMode = doNothing

        # --- Menu --- #
        menubar = tkinter.Menu(self.window)
        fileMenu = tkinter.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open", command=(lambda : self.onMenuFileOpen(filedialog.askdirectory())))
        menubar.add_cascade(label="File", menu=fileMenu)
        self.window.config(menu=menubar)

        # --- Panels --- #
        self.rootPanel = tkinter.PanedWindow()
        self.rootPanel.pack(fill=tkinter.BOTH)

        self.provinceInfoPanel = tkinter.PanedWindow(self.rootPanel, bd=4, relief=RAISED, orient=VERTICAL, width=250)
        self.provinceInfoPanel.pack(fill=tkinter.Y)

        # --- Header --- #
        self.provinceHeader = tkinter.PanedWindow(self.provinceInfoPanel, bd=2)
        self.provinceHeader.pack(side=tkinter.TOP)
        self.provinceIdText = tkinter.StringVar()
        self.provinceIdText.set("No Province Selected")
        self.provinceNameText = tkinter.StringVar()
        self.provinceNameText.set("No Province Selected")
        self.provinceColorText = tkinter.StringVar()
        self.provinceColorText.set("Red: -- Green: -- Blue: --")
        self.provinceIdLabel = tkinter.Label(self.provinceHeader, textvariable=self.provinceIdText)
        self.provinceIdLabel.pack(side=tkinter.TOP)
        self.provinceNameLabel = tkinter.Label(self.provinceHeader, textvariable=self.provinceNameText)
        self.provinceNameLabel.pack(side=tkinter.TOP)
        self.provinceColorLabel = tkinter.Label(self.provinceHeader, textvariable=self.provinceColorText)
        self.provinceColorLabel.pack(side=tkinter.TOP)
        self.provinceInfoPanel.add(self.provinceHeader)

        # --- Body --- #
        self.provinceBody = tkinter.PanedWindow(self.provinceInfoPanel, orient=HORIZONTAL)
        self.provinceBody.pack(side=tkinter.TOP)

        # --- Body-Left --- #
        self.provinceBodyLeft = tkinter.PanedWindow(self.provinceBody, orient=VERTICAL)
        self.provinceBodyLeft.pack(side=tkinter.LEFT)
        self.provinceBody.add(self.provinceBodyLeft)

        self.religions = ["catholicism", "hinduism", "inti"]
        self.religionText = tkinter.Label(self.provinceBodyLeft, text="Religion")
        self.religionText.pack(side=tkinter.TOP)
        self.religionField = AutocompleteCombobox(self.provinceBodyLeft, width=12, completevalues=self.religions)
        self.religionField.pack(side=tkinter.TOP)

        self.cultures = ["outremer", "coomian", "fraszi"]
        self.cultureText = tkinter.Label(self.provinceBodyLeft, text="Culture")
        self.cultureText.pack(side=tkinter.TOP)
        self.cultureField = AutocompleteCombobox(self.provinceBodyLeft, width=12, completevalues=self.cultures)
        self.cultureField.pack(side=tkinter.TOP)

        self.devText = tkinter.Label(self.provinceBodyLeft, text="Admin | Diplo | Mnpwr")
        self.devText.pack(side=tkinter.TOP)
        self.devPanel = tkinter.PanedWindow(self.provinceBodyLeft, orient=HORIZONTAL)
        self.devPanel.pack(side=tkinter.TOP)
        self.taxText = tkinter.Text(self.devPanel, height=1, width=3)
        self.productionText = tkinter.Text(self.devPanel, height=1, width=3)
        self.manpowerText = tkinter.Text(self.devPanel, height=1, width=3)
        self.taxText.pack(side=tkinter.LEFT, padx=(5, 5))
        self.productionText.pack(side=tkinter.LEFT, padx=(5, 5))
        self.manpowerText.pack(side=tkinter.LEFT, padx=(5, 5))

        self.tradeGoods = ["Grain", "Gold", "Cum"]
        self.tradeGoodText = tkinter.Label(self.provinceBodyLeft, text="Trade Good")
        self.tradeGoodText.pack(side=tkinter.TOP)
        self.tradeGoodField = AutocompleteCombobox(self.provinceBodyLeft, width=12, completevalues=self.tradeGoods)
        self.tradeGoodField.pack(side=tkinter.TOP)

        # --- Body-Right --- #
        self.provinceBodyRight = tkinter.PanedWindow(self.provinceBody, orient=VERTICAL)
        self.provinceBodyRight.pack(side=tkinter.LEFT)
        self.provinceBody.add(self.provinceBodyRight)

        self.terrains = ["Farmland" , "Mountains", "Woodlands", "Ocean"]
        self.terrainText = tkinter.Label(self.provinceBodyRight, text="Terrain")
        self.terrainText.pack(side=tkinter.TOP)
        self.terrainField = AutocompleteCombobox(self.provinceBodyRight, completevalues=self.terrains)
        self.terrainField.pack(side=tkinter.TOP)

        self.climates = ["Temperate", "Arctic", "Tropical", "Arid"]
        self.climateText = tkinter.Label(self.provinceBodyRight, text="Climate")
        self.climateText.pack(side=tkinter.TOP)
        self.climateField = AutocompleteCombobox(self.provinceBodyRight, completevalues=self.climates)
        self.climateField.pack(side=tkinter.TOP)

        self.tagText = tkinter.Label(self.provinceBodyRight, text="Owner")
        self.tagText.pack(side=tkinter.TOP)
        self.tagField = tkinter.Text(self.provinceBodyRight, height=1, width=3)
        self.tagField.pack(side=tkinter.TOP)

        self.coresText = tkinter.Label(self.provinceBodyRight, text="Cores")
        self.coresText.pack(side=tkinter.TOP)
        self.coresField = tkinter.Text(self.provinceBodyRight, height=1, width=9)
        self.coresField.pack(side=tkinter.TOP)

        self.areaText = tkinter.Label(self.provinceBodyRight, text="Area")
        self.areaText.pack(side=tkinter.TOP)
        self.areaField = tkinter.Text(self.provinceBodyRight, height=1, width=16)
        self.areaField.pack(side=tkinter.TOP)

        # --- Discovered By --- #
        # Tech groups exist in the technology.txt file in common. Create these dynamically
        self.discoveredByPanel = tkinter.PanedWindow(self.provinceBody, orient=VERTICAL)
        self.discoveredByPanel.pack(side=tkinter.TOP)
        self.provinceBody.add(self.discoveredByPanel)

        self.provinceInfoPanel.add(self.provinceBody)
        self.rootPanel.add(self.provinceInfoPanel)

        #provinceNameLabel.pack(side=tkinter.LEFT)
        #provinceColorLabel.pack(side=tkinter.LEFT)
        #self.infoPanel.add(provinceNameLabel)
        #self.infoPanel.add(provinceColorLabel)

        self.mapDisplay = ScrollableImage(self.rootPanel, width=1024, height=1024)
        self.mapDisplay.pack()
        self.rootPanel.add(self.mapDisplay)

    def updateMap(self, image):
        self.mapDisplay.updateImage(ImageTk.PhotoImage(image))

    def updateProvinceInfo(self, province):
        self.provinceNameText.set("Province: {}".format(province.name))
        self.provinceColorText.set("Red: {} Green: {} Blue: {}".format(province.color[0], province.color[1], province.color[2]))

    def startMainLoop(self):
        self.window.mainloop()