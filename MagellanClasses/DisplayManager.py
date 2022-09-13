import tkinter
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import HORIZONTAL, RAISED, VERTICAL, filedialog
from .ScrollableImage import ScrollableImage
from .Defaults import *
from PIL import ImageTk

def doNothing(*argv):
    pass

def printCallback(*argv):
    print("hi")

class DisplayManager():
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.geometry("1024x776")
        self.window.title("Magellan EU4") # TODO: Change title with mod folder name?
        self.window.protocol('WM_DELETE_WINDOW', self.onClose)

        # The following must be populated
        self.onMenuFileOpen = doNothing
        self.onMenuFileSave = doNothing
        self.onNewMapMode = doNothing
        self.onFieldUpdate = doNothing

        self.rootPanel = tkinter.PanedWindow()
        self.rootPanel.pack(fill=tkinter.BOTH)
        self.createMenubar()
        self.createProvinceInfoPanel()
        self.createScrollableImage()
        self.rootPanel.add(self.provinceInfoPanel)
        self.rootPanel.add(self.mapDisplay)

    def createMenubar(self):
        menubar = tkinter.Menu(self.window)
        fileMenu = tkinter.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open", command=(lambda : self.onMenuFileOpen(filedialog.askdirectory())))
        fileMenu.add_command(label="Save", command=(lambda : self.onMenuFileSave()))
        menubar.add_cascade(label="File", menu=fileMenu)

        self.mapModeMenu = tkinter.Menu(menubar, tearoff=0)
        self.mapModeMenu.add_command(label="Provinces", command=(lambda : self.onNewMapMode("province")))
        self.mapModeMenu.add_command(label="Religions", command=(lambda : self.onNewMapMode("religion")))
        self.mapModeMenu.add_command(label="Cultures", command=(lambda : self.onNewMapMode("culture")))
        self.mapModeMenu.add_command(label="Tax", command=(lambda : self.onNewMapMode("tax")))
        self.mapModeMenu.add_command(label="Production", command=(lambda : self.onNewMapMode("production")))
        self.mapModeMenu.add_command(label="Manpower", command=(lambda : self.onNewMapMode("manpower")))
        self.mapModeMenu.add_command(label="Total Development", command=(lambda : self.onNewMapMode("development")))
        self.mapModeMenu.add_command(label="Trade Goods", command=(lambda : self.onNewMapMode("tradeGood")))
        self.mapModeMenu.add_command(label="Areas", command=(lambda : self.onNewMapMode("area")))
        self.mapModeMenu.add_command(label="Continents", command=(lambda : self.onNewMapMode("continent")))
        self.mapModeMenu.add_command(label="HRE", command=(lambda : self.onNewMapMode("hre")))
        self.mapModeMenu.add_command(label="Owners", command=(lambda : self.onNewMapMode("owner")))
        self.mapModeMenu.add_command(label="Controllers", command=(lambda : self.onNewMapMode("controller")))
        self.mapModeMenu.add_command(label="Terrains", command=(lambda : self.onNewMapMode("terrain")))
        self.mapModeMenu.add_command(label="Climates", command=(lambda : self.onNewMapMode("climate")))
        self.mapModeMenu.add_command(label="Weathers", command=(lambda : self.onNewMapMode("weather")))
        self.mapModeMenu.add_command(label="Trade Nodes", command=(lambda : self.onNewMapMode("tradeNode")))
        self.mapModeMenu.add_command(label="Impassables", command=(lambda : self.onNewMapMode("impassable")))
        self.mapModeMenu.add_separator()
        menubar.add_cascade(label="Map Modes", menu=self.mapModeMenu)
        self.window.config(menu=menubar)

    def createProvinceInfoPanel(self):
        self.provinceInfoPanel = tkinter.PanedWindow(self.rootPanel, bd=4, relief=RAISED, orient=VERTICAL, width=300)
        self.provinceInfoPanel.pack(fill=tkinter.Y)
        self.createProvinceBodyHeader()
        self.createProvinceBodyPanel()
        self.createProvinceBodyFooter()
        self.provinceInfoPanel.add(self.provinceHeader)
        self.provinceInfoPanel.add(self.provinceBody)
        self.provinceInfoPanel.add(self.provinceFooter)

    def createProvinceBodyHeader(self):
        self.provinceHeader = tkinter.PanedWindow(self.provinceInfoPanel, bd=2)
        self.provinceHeader.pack(side=tkinter.TOP)
        self.provinceIdSv = tkinter.StringVar()
        self.provinceIdSv.set("No Province Selected")
        self.provinceNameSv = tkinter.StringVar()
        self.provinceNameSv.set("No Province Selected")
        self.provinceLocalizationNameSv = tkinter.StringVar()
        self.provinceLocalizationNameSv.set("No Province Selected")
        self.provinceLocalizationAdjectiveSv = tkinter.StringVar()
        self.provinceLocalizationAdjectiveSv.set("No Province Selected")
        self.provinceColorSv = tkinter.StringVar()
        self.provinceColorSv.set("Red: -- Green: -- Blue: --")
        self.provinceIdLabel = tkinter.Label(self.provinceHeader, textvariable=self.provinceIdSv)
        self.provinceIdLabel.pack(side=tkinter.TOP)
        self.provinceNameLabel = tkinter.Label(self.provinceHeader, textvariable=self.provinceNameSv)
        self.provinceNameLabel.pack(side=tkinter.TOP)
        self.provinceLocalizationPanel = tkinter.PanedWindow(self.provinceHeader)
        self.provinceLocalizationPanel.pack(side=tkinter.TOP)
        self.provinceLocalizationName = tkinter.Entry(self.provinceLocalizationPanel, width=14, justify="center", textvariable=self.provinceLocalizationNameSv)
        self.provinceLocalizationName.pack(side=tkinter.LEFT)
        self.provinceLocalizationAdjective = tkinter.Entry(self.provinceLocalizationPanel, width=14, justify="center", textvariable=self.provinceLocalizationAdjectiveSv)
        self.provinceLocalizationAdjective.pack(side=tkinter.LEFT)
        self.provinceColorLabel = tkinter.Label(self.provinceHeader, textvariable=self.provinceColorSv)
        self.provinceColorLabel.pack(side=tkinter.TOP)

    def createProvinceBodyPanel(self):
        self.provinceBody = tkinter.PanedWindow(self.provinceInfoPanel, orient=HORIZONTAL)
        self.provinceBody.pack(side=tkinter.TOP)
        self.createLeftProvinceBodyPanel()
        self.createRightProvinceBodyPanel()
        self.provinceBody.add(self.provinceBodyLeft)
        self.provinceBody.add(self.provinceBodyRight)

    def createProvinceBodyFooter(self):
        self.provinceFooter = tkinter.PanedWindow(self.provinceInfoPanel, bd=2)
        self.provinceFooter.pack(side=tkinter.TOP)
        self.provinceFooterHeader = tkinter.Label(self.provinceFooter, text="Discovered By:")
        self.provinceFooterHeader.pack(side=tkinter.TOP)
        self.techGroupToCheckbox = None
        self.checkBoxPanels = None
        self.createNewDiscoveryCheckboxes(DEFAULT_TECH_GROUPS)

    def createNewDiscoveryCheckboxes(self, techGroups):
        self.currentTechGroups = techGroups
        if self.techGroupToCheckbox:
            for checkbox in self.techGroupToCheckbox.keys():
                self.techGroupToCheckbox[checkbox].destroy()
                self.mapModeMenu.delete(checkbox)
        if self.checkBoxPanels:
            for panel in self.checkBoxPanels:
                panel.destroy()
        self.techGroupToCheckbox = dict()
        self.techGroupToIntVar = dict()
        self.checkBoxPanels = []
        currentPanel = None
        rowIndex = 0
        for techGroup in techGroups:
            self.mapModeMenu.add_command(label=techGroup, command=(lambda n=techGroup: self.onNewMapMode(n)))
            if rowIndex == 0:
                currentPanel = tkinter.PanedWindow(self.provinceFooter, orient=HORIZONTAL)
                currentPanel.pack(side=tkinter.TOP)
                self.checkBoxPanels.append(currentPanel)
            techGroupVar = tkinter.IntVar()
            currentCheckbox = tkinter.Checkbutton(currentPanel, variable=techGroupVar, text=techGroup)
            currentCheckbox.pack(side=tkinter.LEFT)
            self.techGroupToCheckbox[techGroup] = currentCheckbox
            self.techGroupToIntVar[techGroup] = techGroupVar
            rowIndex += 1
            if rowIndex == 3:
                rowIndex = 0

    def createLeftProvinceBodyPanel(self):
        self.provinceBodyLeft = tkinter.PanedWindow(self.provinceBody, orient=VERTICAL)
        self.provinceBodyLeft.pack(side=tkinter.LEFT)

        self.capitalSv, self.capitalLabel, self.capitalField = self.createNewEntry("Capital", self.provinceBodyLeft)
        self.religionSv, self.religionLabel, self.religionField = self.createNewAutocompletecombobox("Religion", self.provinceBodyLeft, list(DEFAULT_RELIGIONS.keys()))
        self.cultureSv, self.cultureLabel, self.cultureField = self.createNewAutocompletecombobox("Culture", self.provinceBodyLeft, DEFAULT_CULTURES)

        self.devText = tkinter.Label(self.provinceBodyLeft, text="Adm | Dip | Mil")
        self.devText.pack(side=tkinter.TOP)
        self.devPanel = tkinter.PanedWindow(self.provinceBodyLeft, orient=HORIZONTAL)
        self.devPanel.pack(side=tkinter.TOP)
        self.taxSv, self.taxText = self.createNewDevelopmentEntry("Tax", self.devPanel)
        self.productionSv, self.productionText = self.createNewDevelopmentEntry("Production", self.devPanel)
        self.manpowerSv, self.manpowerText = self.createNewDevelopmentEntry("Manpower", self.devPanel)
        
        self.tradeGoodSv, self.tradeGoodLabel, self.tradeGoodField = self.createNewAutocompletecombobox("Trade Good", self.provinceBodyLeft, DEFAULT_TRADE_GOODS)
        self.areaSv, self.areaLabel, self.areaField = self.createNewEntry("Area", self.provinceBodyLeft)
        self.continentSv, self.continentLabel, self.continentField = self.createNewAutocompletecombobox("Continent", self.provinceBodyLeft, DEFAULT_CONTINENTS)
        self.hreState = tkinter.IntVar()
        self.hreBox = tkinter.Checkbutton(self.provinceBodyLeft, variable=self.hreState, text="HRE")
        self.hreBox.pack(side=tkinter.TOP)

    def createRightProvinceBodyPanel(self):
        self.provinceBodyRight = tkinter.PanedWindow(self.provinceBody, orient=VERTICAL)
        self.provinceBodyRight.pack(side=tkinter.LEFT)

        self.ownerSv, self.ownerLabel, self.ownerField = self.createNewEntry("Owner", self.provinceBodyRight)
        self.controllerSv, self.controllerLabel, self.controllerField = self.createNewEntry("Controller", self.provinceBodyRight)
        self.coresSv, self.coresLabel, self.coresField = self.createNewEntry("Cores", self.provinceBodyRight)
        self.terrainSv, self.terrainLabel, self.terrainField = self.createNewAutocompletecombobox("Terrain", self.provinceBodyRight, DEFAULT_TERRAINS)
        self.climateSv, self.climateLabel, self.climateField = self.createNewAutocompletecombobox("Climate", self.provinceBodyRight, DEFAULT_CLIMATES)
        self.weatherSv, self.weatherLabel, self.weatherField = self.createNewAutocompletecombobox("Weather", self.provinceBodyRight, DEFAULT_WEATHERS)
        self.tradeNodeSv, self.tradeNodeLabel, self.tradeNodeField = self.createNewAutocompletecombobox("Trade Node", self.provinceBodyRight, [])

        self.impassableState = tkinter.IntVar()
        self.impassableBox = tkinter.Checkbutton(self.provinceBodyRight, variable=self.impassableState, text="Impassable")
        self.impassableBox.pack(side=tkinter.TOP)

    def createScrollableImage(self):
        self.mapDisplay = ScrollableImage(self.rootPanel, width=1024, height=1024)
        self.mapDisplay.pack()

    # --- Helpers --- #

    def createNewEntry(self, fieldString, panel):
        stringVar, label = self.createStringVarAndLabel(fieldString, panel)
        entry = tkinter.Entry(panel, textvariable=stringVar, width=12, justify="center")
        entry.pack(side=tkinter.TOP)
        return stringVar, label, entry

    def createNewDevelopmentEntry(self, mapModeString, panel):
        stringVar = tkinter.StringVar()
        stringVar.trace_add("write", (lambda name, index, mode : self.onFieldUpdate(mapModeString, stringVar.get())))
        entry = tkinter.Entry(panel, width=3, justify="center")
        entry.pack(side=tkinter.LEFT, padx=(5, 5))
        return stringVar, entry

    def createNewAutocompletecombobox(self, fieldString, panel, completeValues):
        stringVar, label = self.createStringVarAndLabel(fieldString, panel)
        combobox = AutocompleteCombobox(panel, textvariable=stringVar, completevalues=completeValues)
        combobox.pack(side=tkinter.TOP)
        return stringVar, label, combobox

    def createStringVarAndLabel(self, fieldString, panel):
        mapModeString = fieldString[0].lower() + fieldString[1:].replace(' ', '')
        stringVar = tkinter.StringVar()
        stringVar.trace_add("write", (lambda name, index, mode : self.onFieldUpdate(mapModeString, stringVar.get())))
        label = tkinter.Label(panel, text=fieldString)
        label.pack(side=tkinter.TOP)
        return stringVar, label

    # --- Private Methods --- #

    def onClose(self):
        response = tkinter.messagebox.askyesno('Exit', 'Save your data before you exit?')
        if response:
            self.onMenuFileSave()
        self.window.destroy()

    # --- Public Methods --- #

    def updateMapMode(self, mapMode):
        self.mapDisplay.updateImage(ImageTk.PhotoImage(mapMode.image))

    def updateProvinceInfo(self, province):
        self.provinceIdSv.set("Id: {}".format(province.id))
        self.provinceNameSv.set("{}".format(province.name))
        self.provinceLocalizationNameSv.set(province.localizationName)
        self.provinceLocalizationAdjectiveSv.set(province.localizationAdjective)
        self.provinceColorSv.set("Red: {} Green: {} Blue: {}".format(province.color[0], province.color[1], province.color[2]))
        self.capitalField.delete('0', tkinter.END)
        self.capitalField.insert(tkinter.END, province.capital)
        self.religionField.set(province.religion)
        self.cultureField.set(province.culture)
        self.taxText.delete('0', tkinter.END)
        self.productionText.delete('0', tkinter.END)
        self.manpowerText.delete('0', tkinter.END)
        self.ownerField.delete('0', tkinter.END)
        self.controllerField.delete('0', tkinter.END)
        self.coresField.delete('0', tkinter.END)
        self.areaField.delete('0', tkinter.END)
        self.taxText.insert(tkinter.END, province.tax)
        self.productionText.insert(tkinter.END, province.production)
        self.manpowerText.insert(tkinter.END, province.manpower)
        self.tradeGoodField.set(province.tradeGood)
        self.hreBox.select() if province.hre else self.hreBox.deselect()
        self.impassableBox.select() if province.impassable else self.impassableBox.deselect()
        self.terrainField.set(province.terrain)
        self.controllerField.insert(tkinter.END, province.controller)
        self.climateField.set(province.climate)
        self.weatherField.set(province.weather)
        self.areaField.insert(tkinter.END, province.area)
        self.continentField.set(province.continent)
        self.ownerField.insert(tkinter.END, province.owner)
        self.tradeNodeField.set(province.tradeNode)
        coresText = ""
        for i in range(0, len(province.cores)):
            coresText += province.cores[i]
            if i+1 < len(province.cores):
                coresText += ", "
        for techGroup in self.currentTechGroups:
            if province.discovered[techGroup]:
                self.techGroupToCheckbox[techGroup].select()
            else:
                self.techGroupToCheckbox[techGroup].deselect()
        self.coresField.insert(tkinter.END, coresText)

    def startMainLoop(self):
        self.window.mainloop()