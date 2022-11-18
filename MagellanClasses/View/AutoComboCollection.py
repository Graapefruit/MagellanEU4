import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox

class AutoComboCollection():
    def __init__(self, parent, title, defaults, onModification, onDelete):
        self.parent = parent
        self.defaults = defaults
        self.onModification = onModification
        self.onDelete = onDelete
        self.panel = tk.PanedWindow(self.parent, orient=tk.VERTICAL)
        self.panel.pack(side=tk.TOP)

        self.titlePanel = tk.PanedWindow(self.panel, orient=tk.VERTICAL)
        self.titlePanel.pack(side=tk.TOP)
        self.label = tk.Label(self.titlePanel, text=title)
        self.label.pack(side=tk.LEFT)
        self.addButton = tk.Button(self.titlePanel, text="+", command=self.addEntry)
        self.addButton.pack(side=tk.RIGHT)

        self.entriesPanel = tk.PanedWindow(self.panel, orient=tk.VERTICAL)
        self.entriesPanel.pack(side=tk.TOP)
        self.entries = []

    def addEntry(self):
        newEntry = AutoComboCollectionEntry(self, len(self.entries))
        self.entries.append(newEntry)

    def deleteEntry(self, index):
        self.entries.pop(index)

class AutoComboCollectionEntry():
    def __init__(self, parent, index):
        self.index = index
        self.parent = parent
        self.panel = tk.PanedWindow(self.parent.panel, orient=tk.VERTICAL)
        self.panel.pack(side=tk.TOP)
        self.stringVar = tk.StringVar()
        self.stringVar.trace_add("write", (lambda a,b,c : self.parent.onModification(self.index)))
        self.entry = AutocompleteCombobox(self.panel, textvariable=self.stringVar, completevalues=self.parent.defaults)
        self.entry.pack(side=tk.LEFT)
        self.deleteButton = tk.Button(self.panel, text="-", command=self.delete)
        self.deleteButton.pack(side=tk.RIGHT)

    def delete(self):
        self.parent.onDelete(self.index)
        self.entry.destroy()
        self.deleteButton.destroy()
        self.panel.destroy()