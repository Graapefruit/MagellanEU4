from os import listdir
from enum import Enum

from .EU4DataNode import EU4DataNode
# Three Cases:
# 1. key = value
# 2. key = { values ... values }
# 3. key = { key = ... key = ... }


def parseEU4File(filePath):
    return EU4DataNode(None, readDataFile(filePath), 0)





class EU4DataFileReaderState(Enum):
    FIRST_STRING = 1
    SECOND_STRING = 2
    POST_EQUALS = 3

def parseEU4File(filePath):
    dataPath = [EU4DataNode(None)]
    currentStrings = [""]
    currentState = EU4DataFileReaderState.FIRST_STRING
    for char in readDataFile(filePath):
        match currentState:
            case EU4DataFileReaderState.FIRST_STRING:
                if char == ' ':
                    if len(currentStrings[-1]) > 0:
                        currentStrings.append("")
                elif char == '=':
                    newNode = EU4DataNode(mostCompletePreviousString(currentStrings))
                    dataPath[-1].values[currentField] = newNode
                    currentState = EU4DataFileReaderState.POST_EQUALS
                    currentStrings = [""]
                elif char == "}":
                    if len(currentStrings) > 0:
                        dataPath[-1].values = currentStrings
                    dataPath[-1].values.append(currentField)
                    dataPath.pop()
                else:
                    currentField += char

def mostCompletePreviousString(pastStrings):
    for s in range(len(pastStrings)-1, -1, -1):
        if s != "":
            return s
    return ""

def parseEU4Folder(path):
    data = dict()
    for fileName in listdir(path):
        data.update(parseEU4File("{}/{}".format(path, fileName)))
    return data

def readDataFile(path):
    f = open(path, 'r')
    r = ""
    for line in f.readlines():
        r += line.split('#')[0] + '\n'
    return r

# Tests
if __name__ == "__main__":
    fileName = "\"/home/graham/.steam/steam/steamapps/common/Europa Universalis IV/common/tradenodes/\""
