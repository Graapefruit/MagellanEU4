import os
from os.path import exists
import tkinter as tk
import sys
from tokenize import String
from PIL import Image, ImageTk
from ttkwidgets.autocomplete import AutocompleteCombobox

from MagellanClasses.AutoComboCollection import AutoComboCollection
from MagellanClasses.Constants import FLAGS_FOLDER, GFX_FOLDER
from MagellanClasses.Defaults import DEFAULT_CULTURES, DEFAULT_GOVERNMENTS, DEFAULT_RELIGIONS, DEFAULT_TECH_GROUPS
from Utils.Country import Country
from Utils.TkinterUtils import CallbackWrapper, createNewAutocompletecombobox, createNewEntry

lambdaTrue = (lambda a, b, c : True)

class TagInfoPanel():
    def __init__(self, parent):
        self.onFieldUpdate = CallbackWrapper(lambdaTrue)
        self.panel = tk.PanedWindow(parent, bd=4, relief=tk.RAISED, orient=tk.HORIZONTAL, width=300)
        self.panel.pack(fill=tk.Y, side=tk.RIGHT)
        #self.panel.pack_propagate(False)
        parent.add(self.panel)

        self.tagLabel = tk.Label(self.panel, text="TAG", font=36)
        self.tagLabel.pack(side=tk.TOP)
        sys.stdout.flush()
        self.tagFlagPhotoImage = ImageTk.PhotoImage(Image.open("{}/Utils/NO_TAG.png".format(os.getcwd().replace('\\', '/'))))
        self.imageLabel = tk.Label(self.panel, image=self.tagFlagPhotoImage)
        self.imageLabel.pack(side=tk.TOP)

        self.leftPanel = tk.PanedWindow(self.panel, orient=tk.VERTICAL)
        self.leftPanel.pack(side=tk.LEFT)
        self.techGroupSv, self.techGroupTrace, self.techGroupLabel, self.techGroupField = createNewAutocompletecombobox("Technology Group", self.leftPanel, DEFAULT_TECH_GROUPS, lambdaTrue, self.onFieldUpdate)
        self.governmentTypeSv, self.governmentTypeTrace, self.governmentTypeLabel, self.governmentTypeField = createNewAutocompletecombobox("Government Type", self.leftPanel, DEFAULT_GOVERNMENTS, lambdaTrue, self.onFieldUpdate)
        self.governmentRankSv, self.governmentRankTrace, self.governmentRankLabel, self.governmentRankField = createNewAutocompletecombobox("Government Rank", self.leftPanel, ["1", "2", "3"], lambdaTrue, self.onFieldUpdate)
        #self.governmentReforms = AutoComboCollection(self.leftPanel, "Government Reforms", ["asd", "fsf"], (lambda i : True), (lambda i : True))
        self.religionSv, self.religionTrace, self.religionLabel, self.religionField = createNewAutocompletecombobox("Religion", self.leftPanel, list(DEFAULT_RELIGIONS.keys()), lambdaTrue, self.onFieldUpdate)
        self.primaryCultureSv, self.primaryCultureTrace, self.primaryCultureLabel, self.primaryCultureField = createNewAutocompletecombobox("Primary Culture", self.leftPanel, DEFAULT_CULTURES, lambdaTrue, self.onFieldUpdate)
        #self.acceptedCultures = AutoComboCollection(self.leftPanel, "Accepted Cultures", DEFAULT_CULTURES, (lambda i : True), (lambda i : True))

        self.rightPanel = tk.PanedWindow(self.panel, orient=tk.VERTICAL)
        self.rightPanel.pack(side=tk.LEFT)
        self.capitalSv, self.capitalTrace, self.capitalLabel, self.capitalField = createNewEntry("Capital", self.rightPanel, lambdaTrue, self.onFieldUpdate)
        self.fixedCapitalSv, self.fixedCapitalTrace, self.fixedCapitalLabel, self.fixedCapitalField = createNewEntry("Fixed Capital", self.rightPanel, lambdaTrue, self.onFieldUpdate)
        self.mercantilismSv, self.mercantilismTrace, self.mercantilismLabel, self.mercantilismField = createNewEntry("Mercantilism", self.rightPanel, lambdaTrue, self.onFieldUpdate)
        self.nameSv, self.nameTrace, self.nameLabel, self.nameField = createNewEntry("Name", self.rightPanel, lambdaTrue, self.onFieldUpdate)
        self.adjSv, self.adjTrace, self.adjLabel, self.adjField = createNewEntry("Adjective", self.rightPanel, lambdaTrue, self.onFieldUpdate)

        self.copyFromField = AutocompleteCombobox(self.panel, completevalues=[])
        self.copyButton = tk.Button(self.panel, text="Copy Fields from Another Tag", command = (lambda : True))

    def setTag(self, tag: Country, path: String):
        self.tagLabel.config(text=tag.tag)
        imagePath = "{}/{}/{}/{}".format(path, GFX_FOLDER, FLAGS_FOLDER, tag.tag + ".tga")
        if not exists(imagePath):
            imagePath = Image.open("{}/Utils/NO_TAG.png".format(os.getcwd().replace('\\', '/')))
        self.tagFlagPhotoImage = ImageTk.PhotoImage(Image.open(imagePath))
        self.imageLabel.config(image=self.tagFlagPhotoImage)
        self.techGroupField.set(tag.techGroup)
        self.governmentTypeField.set(tag.governmentType)
        self.governmentRankField.set(tag.governmentRank)
        self.religionField.set(tag.religion)
        self.primaryCultureField.set(tag.primaryCulture)
        
        self.capitalField.delete('0', tk.END)
        self.capitalField.insert(tk.END, tag.capital)
        self.fixedCapitalField.delete('0', tk.END)
        self.fixedCapitalField.insert(tk.END, tag.fixedCapital)
        self.mercantilismField.delete('0', tk.END)
        self.mercantilismField.insert(tk.END, tag.mercantilism)
        self.nameField.delete('0', tk.END)
        self.nameField.insert(tk.END, tag.name)
        self.adjField.delete('0', tk.END)
        self.adjField.insert(tk.END, tag.adj)

    def removeTag(self):
        pass

    # Label for Tag
    # Image, label for path, and button to change
    # Color RGB
    # Drop-Down autocomplete for gov, religion, culture, graphical_culture
    # Collapsable for accepted cultures
    # in-line capital, fixed capital, and mercantilism
    # drop-down autocomplee for name, adj1, and adj2
    # Collapsables for idea groups, historical units, monarch names, leader names, ship names, army names, fleet names