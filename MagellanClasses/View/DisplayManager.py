import tkinter
from tkinter import filedialog

from MagellanClasses.Constants import MAP_MODE_DISPLAY_TO_NAME, MAP_MODE_HOTKEYS
from MagellanClasses.Defaults import DEFAULT_TECH_GROUPS
from MagellanClasses.View.ProvinceInfoPanel import ProvinceInfoPanel
from MagellanClasses.View.TagInfoPanel import TagInfoPanel
from .ScrollableImage import ScrollableImage
from PIL import ImageTk

def doNothing(*argv):
    pass

def printCallback(*argv):
    print("hi")

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
        self.onGeneratePositions = doNothing
        self.onPropagateOwnerData = doNothing
        self.onClearProvinceHistoryUpdates = doNothing

        self.rootPanel = tkinter.PanedWindow()
        self.rootPanel.pack(fill=tkinter.BOTH)
        self.createMenubar()
        self.provinceInfoPanel = ProvinceInfoPanel(self.rootPanel)
        self.createScrollableImage()
        self.tagInfoPanel = TagInfoPanel(self.rootPanel)

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
        self.otherToolsMenu.add_command(label="Clear Province History Updates", command=(lambda : self.propagateOwnerData()))
        self.otherToolsMenu.add_command(label="Modify Adjacencies", command=(lambda : tkinter.messagmessageboxe.showinfo("Soon!", "This current feature is a WIP. Stay tuned!")))
        self.otherToolsMenu.add_command(label="Modify Trade Node Flow", command=(lambda : tkinter.messagebox.showinfo("Soon!", "This current feature is a WIP. Stay tuned!")))
        menubar.add_cascade(label="Other Tools", menu=self.otherToolsMenu)
        self.window.config(menu=menubar)

    def createScrollableImage(self):
        self.mapDisplay = ScrollableImage(self.rootPanel, width=750, height=1024)
        self.mapDisplay.pack()
        self.rootPanel.add(self.mapDisplay)

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

    def updateProvinceSelected(self, province, tag):
        pass

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