import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox

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