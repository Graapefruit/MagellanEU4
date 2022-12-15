import tkinter
from tkinter import filedialog

from MagellanClasses.Constants import MAP_MODE_DISPLAY_TO_NAME, MAP_MODE_HOTKEYS
from MagellanClasses.Defaults import DEFAULT_TECH_GROUPS
from MagellanClasses.View.ProvinceInfoPanel import ProvinceInfoPanel
from .ScrollableImage import ScrollableImage
from PIL import ImageTk
from sys import argv

def doNothing(*argv):
    pass

def printCallback(*argv):
    print("hi")

class DisplayManager():
    def __init__(self, x=1350, y=986):
        x = 1350
        y = 986
        if len(argv) >= 3:
            x = int(argv[1])
            y = int(argv[2])
        self.window = tkinter.Tk()
        self.window.geometry("{}x{}".format(x, y))
        self.window.title("Magellan EU4")
        self.window.protocol('WM_DELETE_WINDOW', self.onClose)

        # The following must be populated
        self.onMenuFileOpen = doNothing
        self.onMenuFileSave = doNothing
        self.onNewMapMode = doNothing
        self.onGeneratePositions = doNothing
        self.onPropagateOwnerData = doNothing
        self.onClearProvinceHistoryUpdates = doNothing
        self.onUpdateProvinceHistoryFileNames = doNothing

        self.rootPanel = tkinter.PanedWindow()
        self.rootPanel.pack(fill=tkinter.BOTH)
        self.createMenubar()
        self.provinceInfoPanel = ProvinceInfoPanel(self.rootPanel)
        self.createScrollableImage(x, y)

        self.mapModes = []

        self.updateAvailableMapModes(DEFAULT_TECH_GROUPS)

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
        self.otherToolsMenu.add_command(label="Clear Province History Date-Updates", command=(lambda : self.clearProvinceHistoryUpdates()))
        self.createToolMenuCommand(self.otherToolsMenu, "Update Province History File Names", "This tool will iterate through all provinces, and rename their corresponding province history file to match the \"<id> - <name>\" convention.\nNote that this might cause issues for non-total conversion mods.", (lambda : self.onUpdateProvinceHistoryFileNames()))
        menubar.add_cascade(label="Other Tools", menu=self.otherToolsMenu)
        self.window.config(menu=menubar)

    def createToolMenuCommand(self, menu, name, text, function):
        menu.add_command(label=name, command=(lambda : (function() if tkinter.messagebox.askyesno(name, text) else None)))

    def createScrollableImage(self, x, y):
        self.mapDisplay = ScrollableImage(self.rootPanel, width=x-400, height=y)
        self.mapDisplay.pack()
        self.rootPanel.add(self.mapDisplay)

    def generatePositions(self):
        result = tkinter.messagebox.askyesno("Generate Positions", "This tool will modify your positions.txt file (if it exists) to add entries for all provinces, setting the average pixel as the position for everything. It will not overwrite existing entries")
        if result:
            self.onGeneratePositions()

    def propagateOwnerData(self):
        result = tkinter.messagebox.askyesno("Propagate Owner Data", "This tool will iterate through every province. If it has a designated owner, it will set the controller to that owner if not already set, and add a core for the owner if no provinces have no current cores. If it has no designated owner, it will remove all cores and the controller.")
        if result:
            self.onPropagateOwnerData()

    def clearProvinceHistoryUpdates(self):
        result = tkinter.messagebox.askyesno("Propagate Owner Data", "This tool will iterate through every province and remove EVERY province history update (ex 1444.12.22 = {{...}}).")
        if result:
            self.onClearProvinceHistoryUpdates()

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
        
    def updateAvailableMapModes(self, newMapModes):
        for mapMode in self.mapModes:
            self.mapModeMenu.delete(mapMode)
        self.provinceInfoPanel.purgeMapModeCheckboxes()

        for mapMode in newMapModes:
            self.mapModeMenu.add_command(label=mapMode, command=(lambda n=mapMode: self.onNewMapMode(n)))
        self.provinceInfoPanel.createNewDiscoveryCheckboxes(newMapModes)
        self.mapModes = newMapModes

    def startMainLoop(self):
        self.window.mainloop()