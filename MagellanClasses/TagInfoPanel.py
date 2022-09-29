import os
from os.path import exists
import tkinter as tk
import sys
from PIL import Image, ImageTk
from ttkwidgets.autocomplete import AutocompleteCombobox

from MagellanClasses.AutoComboCollection import AutoComboCollection
from MagellanClasses.Defaults import DEFAULT_CULTURES, DEFAULT_GOVERNMENTS, DEFAULT_RELIGIONS, DEFAULT_TECH_GROUPS
from Utils.TkinterUtils import CallbackWrapper, createNewAutocompletecombobox, createNewEntry

lambdaTrue = (lambda : True)

class TagInfoPanel():
    def __init__(self, parent):
        self.onFieldUpdate = CallbackWrapper(lambdaTrue)
        self.panel = tk.PanedWindow(parent, bd=4, relief=tk.RAISED, orient=tk.HORIZONTAL, width=300)
        self.panel.pack(fill=tk.Y, side=tk.RIGHT)
        self.panel.pack_propagate(False)
        parent.add(self.panel)

        self.tagLabel = tk.Label(self.panel, text="TAG", font=36)
        self.tagLabel.pack(side=tk.TOP)
        sys.stdout.flush()
        self.tagFlagPhotoImage = ImageTk.PhotoImage(Image.open("{}/Utils/NO_TAG.png".format(os.getcwd().replace('\\', '/'))))
        self.imageLabel = tk.Label(self.panel, image=self.tagFlagPhotoImage)
        self.imageLabel.pack(side=tk.TOP)

        self.changeImageButton = tk.Button(self.panel, text="Change Tag Image", command=(lambda : True))
        self.changeImageButton.pack(side=tk.TOP)

        self.leftPanel = tk.PanedWindow(self.panel, orient=tk.VERTICAL)
        self.leftPanel.pack(side=tk.LEFT)
        self.governmentTypeSv, self.governmentTypeTrace, self.governmentTypeLabel, self.governmentTypeField = createNewAutocompletecombobox("Government Type", self.leftPanel, DEFAULT_GOVERNMENTS, lambdaTrue, self.onFieldUpdate)
        self.governmentRankSv, self.governmentRankTrace, self.governmentRankLabel, self.governmentRankField = createNewAutocompletecombobox("Government Rank", self.leftPanel, ["1", "2", "3"], lambdaTrue, self.onFieldUpdate)
        self.techGroupSv, self.techGroupTrace, self.techGroupLabel, self.techGroupField = createNewAutocompletecombobox("Technology Group", self.leftPanel, DEFAULT_TECH_GROUPS, lambdaTrue, self.onFieldUpdate)
        self.governmentReforms = AutoComboCollection(self.leftPanel, "Government Reforms", ["asd", "fsf"], (lambda i : True), (lambda i : True))
        self.religionSv, self.religionTrace, self.religionLabel, self.religionField = createNewAutocompletecombobox("Religion", self.leftPanel, list(DEFAULT_RELIGIONS.keys()), lambdaTrue, self.onFieldUpdate)
        self.primaryCultureSv, self.primaryCultureTrace, self.primaryCultureLabel, self.primaryCultureField = createNewAutocompletecombobox("Primary Culture", self.leftPanel, DEFAULT_CULTURES, lambdaTrue, self.onFieldUpdate)
        self.acceptedCultures = AutoComboCollection(self.leftPanel, "Accepted Cultures", DEFAULT_CULTURES, (lambda i : True), (lambda i : True))

        self.rightPanel = tk.PanedWindow(self.panel, orient=tk.VERTICAL)
        self.rightPanel.pack(side=tk.LEFT)
        self.capitalSv, self.capitalTrace, self.capitalLabel, self.capitalField = createNewEntry("Capital", self.rightPanel, lambdaTrue, self.onFieldUpdate)
        self.fixedCapitalSv, self.fixedCapitalTrace, self.fixedCapitalLabel, self.fixedCapitalField = createNewEntry("Fixed Capital", self.rightPanel, lambdaTrue, self.onFieldUpdate)
        self.mercantilismSv, self.mercantilismTrace, self.mercantilismLabel, self.mercantilismField = createNewEntry("Mercantilism", self.rightPanel, lambdaTrue, self.onFieldUpdate)
        self.nameSv, self.nameTrace, self.nameLabel, self.nameField = createNewEntry("Name", self.rightPanel, lambdaTrue, self.onFieldUpdate)
        self.adj1Sv, self.adj1Trace, self.adj1Label, self.adj1Field = createNewEntry("Adjective 1", self.rightPanel, lambdaTrue, self.onFieldUpdate)
        self.adj2Sv, self.adj2Trace, self.adj2Label, self.adj2Field = createNewEntry("Adjective 2", self.rightPanel, lambdaTrue, self.onFieldUpdate)

        self.copyFromField = AutocompleteCombobox(self.panel, completevalues=[])
        self.copyButton = tk.Button(self.panel, text="Copy From Above Tag", command = (lambda : True))




    # Label for Tag
    # Image, label for path, and button to change
    # Color RGB
    # Drop-Down autocomplete for gov, religion, culture, graphical_culture
    # Collapsable for accepted cultures
    # in-line capital, fixed capital, and mercantilism
    # drop-down autocomplee for name, adj1, and adj2
    # Collapsables for idea groups, historical units, monarch names, leader names, ship names, army names, fleet names