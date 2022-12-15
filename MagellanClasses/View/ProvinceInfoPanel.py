import tkinter as tk
from PIL import Image, ImageTk
from MagellanClasses.Constants import NO_FLAG_PATH
from MagellanClasses.Defaults import *
from Utils.TkinterUtils import *
from os.path import exists

def doNothing(*argv):
    pass

def noSanityCheck(fieldValue):
    return True

def tagSanityCheck(tag):
    return len(tag)==3 or len(tag)==0

def coreSanityCheck(tags):
    for core in tags.split(','):
        if len(core.strip()) not in [0, 3]:
            return False
    return True

class ProvinceInfoPanel:
    def __init__(self, root):
        self.rootPanel = root
        self.stringVars = []
        self.traceMethods = []
        self.magellanFields = []
        self.flagImagePath = "/"
        self.onFieldUpdate = CallbackWrapper(doNothing)
        self.panel = tk.PanedWindow(self.rootPanel, bd=4, relief=tk.RAISED, orient=tk.VERTICAL, width=300)
        self.scrollbar = tk.Scrollbar(self.panel)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.Y)
        self.panel.pack(fill=tk.Y)
        self.panel.pack_propagate(False)
        self.createProvinceBodyHeader()
        self.createProvinceBodyPanel()
        self.createProvinceBodyFooter()
        self.panel.add(self.provinceHeader)
        self.panel.add(self.provinceBody)
        self.panel.add(self.provinceFooter)
        self.rootPanel.add(self.panel)
        self.scrollbar.config(command = self.panel)

    def createProvinceBodyHeader(self):
        self.provinceHeader = tk.PanedWindow(self.panel, bd=2)
        self.provinceHeader.pack(side=tk.TOP)
        self.provinceIdSv = tk.StringVar()
        self.provinceIdSv.set("No Province Selected")
        self.provinceColorSv = tk.StringVar()
        self.provinceColorSv.set("Red: -- Green: -- Blue: --")
        self.provinceIdLabel = tk.Label(self.provinceHeader, textvariable=self.provinceIdSv)
        self.provinceIdLabel.pack(side=tk.TOP)
        self.magellanFields.append(MagellanEntryField("Name", self.provinceHeader, noSanityCheck, self.onFieldUpdate, packSide=tk.TOP))
        self.provinceLocalizationPanel = tk.PanedWindow(self.provinceHeader)
        self.provinceLocalizationPanel.pack(side=tk.TOP)
        self.magellanFields.append(MagellanEntryField("Localization Name", self.provinceLocalizationPanel, noSanityCheck, self.onFieldUpdate, packSide=tk.LEFT))
        self.magellanFields.append(MagellanEntryField("Localization Adjective", self.provinceLocalizationPanel, noSanityCheck, self.onFieldUpdate, packSide=tk.LEFT))
        self.provinceColorLabel = tk.Label(self.provinceHeader, textvariable=self.provinceColorSv)
        self.provinceColorLabel.pack(side=tk.TOP)
        self.tagFlagPhotoImage = ImageTk.PhotoImage(Image.open(NO_FLAG_PATH))
        self.imageLabel = tk.Label(self.provinceHeader, image=self.tagFlagPhotoImage)
        self.imageLabel.pack(side=tk.TOP)

    def createProvinceBodyPanel(self):
        self.provinceBody = tk.PanedWindow(self.panel, orient=tk.HORIZONTAL)
        self.provinceBody.pack(side=tk.TOP)
        self.createLeftProvinceBodyPanel()
        self.createRightProvinceBodyPanel()
        self.provinceBody.add(self.provinceBodyLeft)
        self.provinceBody.add(self.provinceBodyRight)

    def createProvinceBodyFooter(self):
        self.provinceFooter = tk.PanedWindow(self.panel, bd=2)
        self.provinceFooter.pack(side=tk.TOP)
        self.provinceFooterHeader = tk.Label(self.provinceFooter, text="Discovered By:")
        self.provinceFooterHeader.pack(side=tk.TOP)
        self.techGroupToCheckbox = None
        self.techGroupToIntVar = None
        self.checkBoxPanels = None

    def purgeMapModeCheckboxes(self):
        if self.techGroupToCheckbox:
            for checkbox in self.techGroupToCheckbox.keys():
                self.techGroupToCheckbox[checkbox].destroy()
        if self.checkBoxPanels:
            for panel in self.checkBoxPanels:
                panel.destroy()

    def createNewDiscoveryCheckboxes(self, techGroups):
        self.currentTechGroups = techGroups
        self.techGroupToCheckbox = dict()
        self.techGroupToIntVar = dict()
        self.techGroupToTrace = dict()
        self.checkBoxPanels = []
        currentPanel = None
        rowIndex = 0
        for techGroup in techGroups:
            if rowIndex == 0:
                currentPanel = tk.PanedWindow(self.provinceFooter, orient=tk.HORIZONTAL)
                currentPanel.pack(side=tk.TOP)
                self.checkBoxPanels.append(currentPanel)
            techGroupVar = tk.IntVar()
            traceMethod = (lambda name, index, mode, techGroup=techGroup, techGroupVar=techGroupVar : self.onFieldUpdate.callback(techGroup, techGroupVar.get(), noSanityCheck))
            techGroupVar.trace_add("write", traceMethod)
            currentCheckbox = tk.Checkbutton(currentPanel, variable=techGroupVar, text=techGroup)
            currentCheckbox.pack(side=tk.LEFT)
            self.techGroupToCheckbox[techGroup] = currentCheckbox
            self.techGroupToIntVar[techGroup] = techGroupVar
            self.techGroupToTrace[techGroup] = traceMethod
            rowIndex += 1
            if rowIndex == 3:
                rowIndex = 0

    def createLeftProvinceBodyPanel(self):
        self.provinceBodyLeft = tk.PanedWindow(self.provinceBody, orient=tk.VERTICAL)
        self.provinceBodyLeft.pack(side=tk.LEFT)

        capitalSv, capitalTrace, self.capitalLabel, self.capitalField = createNewEntry("Capital", self.provinceBodyLeft, noSanityCheck, self.onFieldUpdate)
        religionSv, religionTrace, self.religionLabel, self.religionField = createNewAutocompletecombobox("Religion", self.provinceBodyLeft, list(DEFAULT_RELIGIONS.keys()), noSanityCheck, self.onFieldUpdate)
        cultureSv, cultureTrace, self.cultureLabel, self.cultureField = createNewAutocompletecombobox("Culture", self.provinceBodyLeft, DEFAULT_CULTURES, noSanityCheck, self.onFieldUpdate)

        self.devText = tk.Label(self.provinceBodyLeft, text="Adm | Dip | Mil")
        self.devText.pack(side=tk.TOP)
        self.devPanel = tk.PanedWindow(self.provinceBodyLeft, orient=tk.HORIZONTAL)
        self.devPanel.pack(side=tk.TOP)
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
        self.provinceBodyRight = tk.PanedWindow(self.provinceBody, orient=tk.VERTICAL)
        self.provinceBodyRight.pack(side=tk.LEFT)

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

    def updateProvinceInfo(self, province):
        for magellanField in self.magellanFields:
            magellanField.setField(province)
        self.disableTraceMethods()
        ownerFlagPath = "{}/{}.tga".format(self.flagImagePath, province.owner)
        if not exists(ownerFlagPath):
            ownerFlagPath = NO_FLAG_PATH
        self.tagFlagPhotoImage = ImageTk.PhotoImage(Image.open(ownerFlagPath))
        self.imageLabel.config(image=self.tagFlagPhotoImage)
        self.provinceIdSv.set("Id: {}".format(province.id))
        self.provinceColorSv.set("Red: {} Green: {} Blue: {}".format(province.color[0], province.color[1], province.color[2]))
        self.capitalField.delete('0', tk.END)
        self.capitalField.insert(tk.END, province.capital)
        self.religionField.set(province.religion)
        self.cultureField.set(province.culture)
        self.taxText.delete('0', tk.END)
        self.productionText.delete('0', tk.END)
        self.manpowerText.delete('0', tk.END)
        self.areaField.delete('0', tk.END)
        self.taxText.insert(tk.END, str(province.tax))
        self.productionText.insert(tk.END, str(province.production))
        self.manpowerText.insert(tk.END, str(province.manpower))
        self.tradeGoodField.set(province.tradeGood)
        self.hreBox.select() if province.hre else self.hreBox.deselect()
        self.impassableBox.select() if province.impassable else self.impassableBox.deselect()
        self.isLakeBox.select() if province.isLake else self.isLakeBox.deselect()
        self.isSeaBox.select() if province.isSea else self.isSeaBox.deselect()
        self.terrainField.set(province.terrain)
        self.controllerField.set(province.controller)
        self.climateField.set(province.climate)
        self.weatherField.set(province.weather)
        self.areaField.insert(tk.END, province.area)
        self.continentField.set(province.continent)
        self.ownerField.set(province.owner)
        self.tradeNodeField.set(province.tradeNode)
        self.coresField.delete('0', tk.END)
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
        self.coresField.insert(tk.END, coresText)
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