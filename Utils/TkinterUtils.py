import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
from abc import ABC, abstractmethod

class MagellanField(ABC):
    @abstractmethod
    def setField(self, newValue):
        pass
    def enableTrace(self):
        self.stringVar.trace_remove('write', self.stringVar.trace_info()[0][1])
    def disableTrace(self):
        self.stringVar.trace_add("write", self.traceMethod)

class MagellanEntryField(MagellanField):
    def __init__(self, fieldString, parentPanel, sanityCheck, callbackReference):
        self.mapModeString = getMapModeString(fieldString)
        self.panel = tk.PanedWindow(parentPanel)
        self.panel.pack(side=tk.LEFT)
        self.stringVar, self.traceMethod, self.label = createStringVarAndLabel(fieldString, self.panel, sanityCheck, callbackReference)
        self.entry = tk.Entry(self.panel, textvariable=self.stringVar, width=12, justify="center")
        self.entry.pack(side=tk.TOP)

    def setField(self, province):
        self.enableTrace()
        self.entry.delete('0', tk.END)
        self.entry.insert(tk.END, province.getFieldFromString(self.mapModeString))
        self.disableTrace()

def createNewEntry(fieldString, panel, sanityCheck, callbackReference):
    stringVar, traceMethod, label = createStringVarAndLabel(fieldString, panel, sanityCheck, callbackReference)
    entry = tk.Entry(panel, textvariable=stringVar, width=12, justify="center")
    entry.pack(side=tk.TOP)
    return stringVar, traceMethod, label, entry

def createNewAutocompletecombobox(fieldString, panel, completeValues, sanityCheck, callbackReference):
    stringVar, traceMethod, label = createStringVarAndLabel(fieldString, panel, sanityCheck, callbackReference)
    combobox = AutocompleteCombobox(panel, textvariable=stringVar, completevalues=completeValues)
    combobox.pack(side=tk.TOP)
    return stringVar, traceMethod, label, combobox

def createNewCheckbutton(fieldString, panel, callbackReference):
    mapModeString = getMapModeString(fieldString)
    intVar = tk.IntVar()
    traceMethod = (lambda name, index, mode : callbackReference.callback(mapModeString, intVar.get(), (lambda n : True)))
    intVar.trace_add("write", traceMethod)
    checkButton = tk.Checkbutton(panel, variable=intVar, text=fieldString)
    checkButton.pack(side=tk.TOP)
    return intVar, traceMethod, checkButton

def createStringVarAndLabel(fieldString, panel, sanityCheck, callbackReference):
    mapModeString = getMapModeString(fieldString)
    traceMethod = (lambda name, index, mode : callbackReference.callback(mapModeString, stringVar.get(), sanityCheck))
    stringVar = tk.StringVar()
    stringVar.trace_add("write", traceMethod)
    label = tk.Label(panel, text=fieldString)
    label.pack(side=tk.TOP)
    return stringVar, traceMethod, label

def createNewDevelopmentEntry(fieldString, panel, callbackReference):
    mapModeString = getMapModeString(fieldString)
    stringVar = tk.StringVar()
    traceMethod = (lambda name, index, mode : callbackReference.callback(mapModeString, stringVar.get(), (lambda n : n.isdigit() or n == "")))
    stringVar.trace_add("write", traceMethod, )
    entry = tk.Entry(panel, width=3, justify="center", textvariable=stringVar)
    entry.pack(side=tk.LEFT, padx=(5, 5))
    return stringVar, traceMethod, entry

def getMapModeString(fieldString):
    return fieldString[0].lower() + fieldString[1:].replace(' ', '')

class CallbackWrapper():
    def __init__(self, callback):
        self.callback=callback