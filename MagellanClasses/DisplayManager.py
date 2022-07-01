from logging import root
import sys
import tkinter
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import HORIZONTAL, RAISED, VERTICAL, StringVar, filedialog, ttk
from .ScrollableImage import ScrollableImage
from PIL import ImageTk

def doNothing(*argv):
    pass

def callBack(sv):
    print(sv.get())

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
        self.createProvinceInfoPanel()
        self.createScrollableImage()
        self.rootPanel.add(self.provinceInfoPanel)
        self.rootPanel.add(self.mapDisplay)

    def createProvinceInfoPanel(self):
        self.provinceInfoPanel = tkinter.PanedWindow(self.rootPanel, bd=4, relief=RAISED, orient=VERTICAL, width=300)
        self.provinceInfoPanel.pack(fill=tkinter.Y)
        self.createProvinceBodyHeader()
        self.createProvinceBodyPanel()
        self.provinceInfoPanel.add(self.provinceHeader)
        self.provinceInfoPanel.add(self.provinceBody)

    def createProvinceBodyHeader(self):
        self.provinceHeader = tkinter.PanedWindow(self.provinceInfoPanel, bd=2)
        self.provinceHeader.pack(side=tkinter.TOP)
        self.provinceIdSv = tkinter.StringVar()
        self.provinceIdSv.set("No Province Selected")
        self.provinceNameSv = tkinter.StringVar()
        self.provinceNameSv.set("No Province Selected")
        self.provinceColorSv = tkinter.StringVar()
        self.provinceColorSv.set("Red: -- Green: -- Blue: --")
        self.provinceIdLabel = tkinter.Label(self.provinceHeader, textvariable=self.provinceIdSv)
        self.provinceIdLabel.pack(side=tkinter.TOP)
        self.provinceNameLabel = tkinter.Entry(self.provinceHeader, width=12, justify="center", textvariable=self.provinceNameSv)
        self.provinceNameLabel.pack(side=tkinter.TOP)
        self.provinceColorLabel = tkinter.Label(self.provinceHeader, textvariable=self.provinceColorSv)
        self.provinceColorLabel.pack(side=tkinter.TOP)

    def createProvinceBodyPanel(self):
        self.provinceBody = tkinter.PanedWindow(self.provinceInfoPanel, orient=HORIZONTAL)
        self.provinceBody.pack(side=tkinter.TOP)
        self.createLeftProvinceBodyPanel()
        self.createRightProvinceBodyPanel()
        self.provinceBody.add(self.provinceBodyLeft)
        self.provinceBody.add(self.provinceBodyRight)

    def createLeftProvinceBodyPanel(self):
        self.provinceBodyLeft = tkinter.PanedWindow(self.provinceBody, orient=VERTICAL)
        self.provinceBodyLeft.pack(side=tkinter.LEFT)

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

        self.devText = tkinter.Label(self.provinceBodyLeft, text="Adm | Dip | Mil")
        self.devText.pack(side=tkinter.TOP)
        self.devPanel = tkinter.PanedWindow(self.provinceBodyLeft, orient=HORIZONTAL)
        self.devPanel.pack(side=tkinter.TOP)
        self.taxText = tkinter.Entry(self.devPanel, width=3, justify="center")
        self.productionText = tkinter.Entry(self.devPanel, width=3, justify="center")
        self.manpowerText = tkinter.Entry(self.devPanel, width=3, justify="center")
        self.taxText.pack(side=tkinter.LEFT, padx=(5, 5))
        self.productionText.pack(side=tkinter.LEFT, padx=(5, 5))
        self.manpowerText.pack(side=tkinter.LEFT, padx=(5, 5))

        self.tradeGoods = ["Grain", "Gold", "Cum"]
        self.tradeGoodText = tkinter.Label(self.provinceBodyLeft, text="Trade Good")
        self.tradeGoodText.pack(side=tkinter.TOP)
        self.tradeGoodField = AutocompleteCombobox(self.provinceBodyLeft, width=12, completevalues=self.tradeGoods)
        self.tradeGoodField.pack(side=tkinter.TOP)

        self.hreBox = tkinter.Checkbutton(self.provinceBodyLeft, text="HRE")
        self.hreBox.pack(side=tkinter.TOP)

    def createRightProvinceBodyPanel(self):
        self.provinceBodyRight = tkinter.PanedWindow(self.provinceBody, orient=VERTICAL)
        self.provinceBodyRight.pack(side=tkinter.LEFT)

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

        self.areaText = tkinter.Label(self.provinceBodyRight, text="Area")
        self.areaText.pack(side=tkinter.TOP)
        self.areaField = tkinter.Entry(self.provinceBodyRight, justify="center")
        self.areaField.pack(side=tkinter.TOP)

        self.continents = ["Asia", "Europe", "Atlantis"]
        self.continentText = tkinter.Label(self.provinceBodyRight, text="Continent")
        self.continentText.pack(side=tkinter.TOP)
        self.continentField = AutocompleteCombobox(self.provinceBodyRight, completevalues=self.continents)
        self.continentField.pack(side=tkinter.TOP)

        self.tagText = tkinter.Label(self.provinceBodyRight, text="Owner")
        self.tagText.pack(side=tkinter.TOP)
        self.tagField = tkinter.Entry(self.provinceBodyRight, justify="center")
        self.tagField.pack(side=tkinter.TOP)

        self.coresText = tkinter.Label(self.provinceBodyRight, text="Cores")
        self.coresText.pack(side=tkinter.TOP)
        self.coresField = tkinter.Entry(self.provinceBodyRight, justify="center")
        self.coresField.pack(side=tkinter.TOP)

    def createScrollableImage(self):
        self.mapDisplay = ScrollableImage(self.rootPanel, width=1024, height=1024)
        self.mapDisplay.pack()


    def updateMap(self, image):
        self.mapDisplay.updateImage(ImageTk.PhotoImage(image))

    def updateProvinceInfo(self, province):
        self.provinceIdSv.set("Id: {}".format(province.id))
        self.provinceNameSv.set("{}".format(province.name))
        self.provinceColorSv.set("Red: {} Green: {} Blue: {}".format(province.color[0], province.color[1], province.color[2]))
        self.religionField.set(province.religion)
        self.cultureField.set(province.culture)
        #if len(self.taxText.get()) > 0:
        self.taxText.delete('0', tkinter.END)
        self.productionText.delete('0', tkinter.END)
        self.manpowerText.delete('0', tkinter.END)
        self.tagField.delete('0', tkinter.END)
        self.coresField.delete('0', tkinter.END)
        self.taxText.insert(tkinter.END, province.tax)
        self.productionText.insert(tkinter.END, province.tax)
        self.manpowerText.insert(tkinter.END, province.tax)
        self.tradeGoodField.set(province.tradeGood)
        self.hreBox.select if province.hre else self.hreBox.deselect
        # self.terrainField.set()
        # self.climateField.set()
        # self.areaField.set()
        # self.continentField.set()
        self.tagField.insert(tkinter.END, province.owner)
        coresText = ""
        for i in range(0, len(province.cores)):
            coresText += province.cores(i)
            if i+1 < len(province.cores):
                coresText += ", "
        self.coresField.insert(tkinter.END, coresText)

    def startMainLoop(self):
        self.window.mainloop()