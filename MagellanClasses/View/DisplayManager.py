from inspect import trace
import tkinter
from tkinter import HORIZONTAL, RAISED, VERTICAL, filedialog

from MagellanClasses.Constants import MAP_MODE_DISPLAY_TO_NAME, MAP_MODE_HOTKEYS
from MagellanClasses.View.TagInfoPanel import TagInfoPanel
from Utils.TkinterUtils import *
from .ScrollableImage import ScrollableImage
from MagellanClasses.Defaults import *
from PIL import ImageTk

def doNothing(*argv):
    pass

def printCallback(*argv):
    print("hi")

def noSanityCheck(fieldValue):
    return True

def tagSanityCheck(tag):
    return len(tag)==3 or len(tag)==0

def coreSanityCheck(tags):
    for core in tags.split(','):
        if len(core.strip()) != 3:
            return False
    return True

class DisplayManager():
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.geometry("1350x776")
        self.window.title("Magellan EU4")
        self.window.protocol('WM_DELETE_WINDOW', self.onClose)

        # The following must be populated
        self.onMenuFileOpen = doNothing
        self.onMenuFileSave = doNothing
        self.onNewMapMode = doNothing
        self.onFieldUpdate = CallbackWrapper(doNothing)
        self.onGeneratePositions = doNothing
        self.onPropagateOwnerData = doNothing
        self.onClearProvinceHistoryUpdates = doNothing
        
        self.stringVars = []
        self.traceMethods = []

        self.rootPanel = tkinter.PanedWindow()
        self.rootPanel.pack(fill=tkinter.BOTH)
        self.createMenubar()
        self.createProvinceInfoPanel()
        self.createScrollableImage()
        self.createTagInfoPanel()

    def createMenubar(self):
        menubar = tkinter.Menu(self.window)
        fileMenu = tkinter.Menu(menubar, tearoff=0)
        fileMenu.add_command(label="Open", command=(lambda : self.onMenuFileOpen(filedialog.askdirectory())))
        fileMenu.add_command(label="Save", command=(lambda : self.onMenuFileSave()))
        menubar.add_cascade(label="File", menu=fileMenu)

        self.mapModeMenu = tkinter.Menu(menubar, tearoff=0)
        mapModeToHotkey = dict()
        for hotkey in MAP_MODE_HOTKEYS:
            mapModeToHotkey[MAP_MODE_HOTKEYS[hotkey]] = hotkey
        for mapModeDisplayName in MAP_MODE_DISPLAY_TO_NAME.keys():
            displayName = "{} ({})".format(mapModeDisplayName, mapModeToHotkey[MAP_MODE_DISPLAY_TO_NAME[mapModeDisplayName]])
            self.mapModeMenu.add_command(label=displayName, command=(lambda d=mapModeDisplayName : self.onNewMapMode(MAP_MODE_DISPLAY_TO_NAME[d])))
        # TODO: fire the below when not selecting a field
        # self.window.bind('<KeyPress>', (lambda e : self.onNewMapMode(MAP_MODE_HOTKEYS[e.char.upper()])))
        self.mapModeMenu.add_separator()
        menubar.add_cascade(label="Map Modes", menu=self.mapModeMenu)

        self.otherToolsMenu = tkinter.Menu(menubar, tearoff=0)
        self.otherToolsMenu.add_command(label="Generate Positions", command=(lambda : self.generatePositions()))
        self.otherToolsMenu.add_command(label="Propagate Owner Data", command=(lambda : self.propagateOwnerData()))
        self.otherToolsMenu.add_command(label="Clear Province History Updates", command=(lambda : self.propagateOwnerData()))
        self.otherToolsMenu.add_command(label="Modify Adjacencies", command=(lambda : tkinter.messagmessageboxe.showinfo("Soon!", "This current feature is a WIP. Stay tuned!")))
        self.otherToolsMenu.add_command(label="Modify Trade Node Flow", command=(lambda : tkinter.messagebox.showinfo("Soon!", "This current feature is a WIP. Stay tuned!")))
        menubar.add_cascade(label="Other Tools", menu=self.otherToolsMenu)
        self.window.config(menu=menubar)

    def generatePositions(self):
        result = tkinter.messagebox.askyesno("Generate Positions", "This tool will modify your positions.txt file (if it exists) to add entries for all provinces, setting the average pixel as the position for everything. It will not overwrite existing entries")
        if result:
            self.onGeneratePositions()

    def propagateOwnerData(self):
        result = tkinter.messagebox.askyesno("Propagate Owner Data", "This tool will iterate through every province. If it has a designated owner, it will set the controller to that owner if not already set, and add a core for the owner if no provinces have no current cores.")
        if result:
            self.onPropagateOwnerData()

    def propagateOwnerData(self):
        result = tkinter.messagebox.askyesno("Propagate Owner Data", "This tool will iterate through every province and remove EVERY province history update (ex 1444.12.22 = {{...}}).")
        if result:
            self.onClearProvinceHistoryUpdates()

    def createProvinceInfoPanel(self):
        self.provinceInfoPanel = tkinter.PanedWindow(self.rootPanel, bd=4, relief=RAISED, orient=VERTICAL, width=300)
        self.provinceInfoPanel.pack(fill=tkinter.Y)
        self.provinceInfoPanel.pack_propagate(False)
        self.createProvinceBodyHeader()
        self.createProvinceBodyPanel()
        self.createProvinceBodyFooter()
        self.provinceInfoPanel.add(self.provinceHeader)
        self.provinceInfoPanel.add(self.provinceBody)
        self.provinceInfoPanel.add(self.provinceFooter)
        self.rootPanel.add(self.provinceInfoPanel)

    def createTagInfoPanel(self):
        self.tagInfoPanel = TagInfoPanel(self.rootPanel)

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
        self.techGroupToIntVar = None
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
        self.techGroupToTrace = dict()
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
            traceMethod = (lambda name, index, mode, techGroup=techGroup, techGroupVar=techGroupVar : self.onFieldUpdate.callback(techGroup, techGroupVar.get(), noSanityCheck))
            techGroupVar.trace_add("write", traceMethod)
            currentCheckbox = tkinter.Checkbutton(currentPanel, variable=techGroupVar, text=techGroup)
            currentCheckbox.pack(side=tkinter.LEFT)
            self.techGroupToCheckbox[techGroup] = currentCheckbox
            self.techGroupToIntVar[techGroup] = techGroupVar
            self.techGroupToTrace[techGroup] = traceMethod
            rowIndex += 1
            if rowIndex == 3:
                rowIndex = 0

    def createLeftProvinceBodyPanel(self):
        self.provinceBodyLeft = tkinter.PanedWindow(self.provinceBody, orient=VERTICAL)
        self.provinceBodyLeft.pack(side=tkinter.LEFT)

        capitalSv, capitalTrace, self.capitalLabel, self.capitalField = createNewEntry("Capital", self.provinceBodyLeft, noSanityCheck, self.onFieldUpdate)
        religionSv, religionTrace, self.religionLabel, self.religionField = createNewAutocompletecombobox("Religion", self.provinceBodyLeft, list(DEFAULT_RELIGIONS.keys()), noSanityCheck, self.onFieldUpdate)
        cultureSv, cultureTrace, self.cultureLabel, self.cultureField = createNewAutocompletecombobox("Culture", self.provinceBodyLeft, DEFAULT_CULTURES, noSanityCheck, self.onFieldUpdate)

        self.devText = tkinter.Label(self.provinceBodyLeft, text="Adm | Dip | Mil")
        self.devText.pack(side=tkinter.TOP)
        self.devPanel = tkinter.PanedWindow(self.provinceBodyLeft, orient=HORIZONTAL)
        self.devPanel.pack(side=tkinter.TOP)
        taxSv, taxTrace, self.taxText = createNewDevelopmentEntry("Tax", self.devPanel, self.onFieldUpdate)
        productionSv, productionTrace, self.productionText = createNewDevelopmentEntry("Production", self.devPanel, self.onFieldUpdate)
        manpowerSv, manpowerTrace, self.manpowerText = createNewDevelopmentEntry("Manpower", self.devPanel, self.onFieldUpdate)
        
        tradeGoodSv, tradeGoodTrace, self.tradeGoodLabel, self.tradeGoodField = createNewAutocompletecombobox("Trade Good", self.provinceBodyLeft, DEFAULT_TRADE_GOODS, noSanityCheck, self.onFieldUpdate)
        areaSv, areaTrace, self.areaLabel, self.areaField = createNewEntry("Area", self.provinceBodyLeft, noSanityCheck, self.onFieldUpdate)
        continentSv, continentTrace, self.continentLabel, self.continentField = createNewAutocompletecombobox("Continent", self.provinceBodyLeft, DEFAULT_CONTINENTS, noSanityCheck, self.onFieldUpdate)
        hreIv, hreTrace, self.hreBox = createNewCheckbutton("Hre", self.provinceBodyLeft, self.onFieldUpdate)
        isLakeIv, isLakeTrace, self.isLakeBox = createNewCheckbutton("Is Lake", self.provinceBodyLeft, self.onFieldUpdate)

        self.stringVars += [capitalSv, religionSv, cultureSv, taxSv, productionSv, manpowerSv, tradeGoodSv, areaSv, continentSv, hreIv, isLakeIv]
        self.traceMethods += [capitalTrace, religionTrace, cultureTrace, taxTrace, productionTrace, manpowerTrace, tradeGoodTrace, areaTrace, continentTrace, hreTrace, isLakeTrace]

    def createRightProvinceBodyPanel(self):
        self.provinceBodyRight = tkinter.PanedWindow(self.provinceBody, orient=VERTICAL)
        self.provinceBodyRight.pack(side=tkinter.LEFT)

        ownerSv, ownerTrace, self.ownerLabel, self.ownerField = createNewAutocompletecombobox("Owner", self.provinceBodyRight, [], tagSanityCheck, self.onFieldUpdate)
        controllerSv, controllerTrace, self.controllerLabel, self.controllerField = createNewAutocompletecombobox("Controller", self.provinceBodyRight, [], tagSanityCheck, self.onFieldUpdate)
        coresSv, coreTrace, self.coresLabel, self.coresField = createNewEntry("Cores", self.provinceBodyRight, coreSanityCheck, self.onFieldUpdate)
        terrainSv, terrainTrace, self.terrainLabel, self.terrainField = createNewAutocompletecombobox("Terrain", self.provinceBodyRight, DEFAULT_TERRAINS, noSanityCheck, self.onFieldUpdate)
        climateSv, climateTrace, self.climateLabel, self.climateField = createNewAutocompletecombobox("Climate", self.provinceBodyRight, DEFAULT_CLIMATES, noSanityCheck, self.onFieldUpdate)
        weatherSv, weatherTrace, self.weatherLabel, self.weatherField = createNewAutocompletecombobox("Weather", self.provinceBodyRight, DEFAULT_WEATHERS, noSanityCheck, self.onFieldUpdate)
        tradeNodeSv, tradeNodeTrace, self.tradeNodeLabel, self.tradeNodeField = createNewAutocompletecombobox("Trade Node", self.provinceBodyRight, [], noSanityCheck, self.onFieldUpdate)
        impassableIv, impassableTrace, self.impassableBox = createNewCheckbutton("Impassable", self.provinceBodyRight, self.onFieldUpdate)
        isSeaIv, isSeaTrace, self.isSeaBox = createNewCheckbutton("Is Sea", self.provinceBodyRight, self.onFieldUpdate)

        self.stringVars += [ownerSv, controllerSv, coresSv, terrainSv, climateSv, weatherSv, tradeNodeSv, impassableIv, isSeaIv]
        self.traceMethods += [ownerTrace, controllerTrace, coreTrace, terrainTrace, climateTrace, weatherTrace, tradeNodeTrace, impassableTrace, isSeaTrace]

    def createScrollableImage(self):
        self.mapDisplay = ScrollableImage(self.rootPanel, width=750, height=1024)
        self.mapDisplay.pack()
        self.rootPanel.add(self.mapDisplay)

    # --- Private Methods --- #

    def onClose(self):
        response = tkinter.messagebox.askyesnocancel('Exit', 'Save your data before you exit?')
        if response:
            self.onMenuFileSave()
            self.window.destroy()
        elif response == False:
            self.window.destroy()

    # --- Public Methods --- #

    def updateMapMode(self, mapMode):
        self.mapDisplay.updateImage(ImageTk.PhotoImage(mapMode.image))

    def updateProvinceInfo(self, province):
        self.disableTraceMethods()
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
        self.areaField.delete('0', tkinter.END)
        self.taxText.insert(tkinter.END, str(province.tax))
        self.productionText.insert(tkinter.END, str(province.production))
        self.manpowerText.insert(tkinter.END, str(province.manpower))
        self.tradeGoodField.set(province.tradeGood)
        self.hreBox.select() if province.hre else self.hreBox.deselect()
        self.impassableBox.select() if province.impassable else self.impassableBox.deselect()
        self.isLakeBox.select() if province.isLake else self.isLakeBox.deselect()
        self.isSeaBox.select() if province.isSea else self.isSeaBox.deselect()
        self.terrainField.set(province.terrain)
        self.controllerField.set(province.controller)
        self.climateField.set(province.climate)
        self.weatherField.set(province.weather)
        self.areaField.insert(tkinter.END, province.area)
        self.continentField.set(province.continent)
        self.ownerField.set(province.owner)
        self.tradeNodeField.set(province.tradeNode)
        self.coresField.delete('0', tkinter.END)
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
        self.enableTraceMethods()

    def disableTraceMethods(self):
        for i in range(0, len(self.stringVars)):
            self.stringVars[i].trace_remove('write', self.stringVars[i].trace_info()[0][1])
        for techGroup in self.currentTechGroups:
            self.techGroupToIntVar[techGroup].trace_remove('write', self.techGroupToIntVar[techGroup].trace_info()[0][1])

    def enableTraceMethods(self):
        for i in range(0, len(self.stringVars)):
            self.stringVars[i].trace_add("write", self.traceMethods[i])
        for techGroup in self.currentTechGroups:
            self.techGroupToIntVar[techGroup].trace_add("write", self.techGroupToTrace[techGroup])

    def startMainLoop(self):
        self.window.mainloop()