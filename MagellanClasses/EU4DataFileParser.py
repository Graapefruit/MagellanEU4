from os import listdir
from enum import Enum
from os.path import exists
# Three Cases:
# 1. key = value
# 2. key = { values ... values }
# 3. key = { key = ... key = ... }

class EU4DataFileReaderState(Enum):
    FIRST_STRING = 1
    POST_EQUALS = 2
    SECOND_STRING = 3
    IN_QUOTATIONS = 4
    
class EU4DataNode():
    def __init__(self, name):
        self.name = name
        self.values = dict()

    def toString(self):
        return self._toStringHelper(0)

    def getChildren(self):
        return self.values.values()

    def getAndCreateIfNotExists(self, name):
        if not name in self.values:
            self.values[name] = EU4DataNode(name)
        return self.values[name]

    def appendValueOverwriteDict(self, name):
        if isinstance(self.values, dict):
            self.values = [name]
        else:
            self.values.append(name)

    def __getitem__(self, name):
        return self.values[name]

    def __setitem__(self, name, value):
        self.values[name] = value

    def __contains__(self, value):
        return value in self.values

    def _toStringHelper(self, depth):
        s = "\t" * depth + self.name + " = "
        if isinstance(self.values, str):
            s += self.values + '\n'
        elif isinstance(self.values, list):
            s += "{\n" + "\t" * (depth+1)
            for value in self.values:
                s += value + ' '
            s += "\n" + "\t" * depth + "}\n"
        elif isinstance(self.values, dict):
            s += "{\n"
            for child in self.values.values():
                s += child._toStringHelper(depth+1)
            s += "\t" * depth + "}\n"
        else:
            print("WARNING: Values field of {}, {}, is of unrecognized type!".format(self.name, self.values))
        return s

def writeToFileFromRootNode(filePath, rootNode):
    f = open(filePath, 'w')
    for value in rootNode.getChildren():
        f.write(value.toString() + '\n')

def parseEU4File(filePath):
    baseNode = None
    if exists(filePath):
        baseNode = EU4DataNode("__ROOT__")
        dataPath = [baseNode]
        pastStrings = []
        currentString = ''
        currentState = EU4DataFileReaderState.FIRST_STRING
        for char in readDataFile(filePath):
            match currentState:
                case EU4DataFileReaderState.FIRST_STRING:
                    # Spaces are separators between words
                    if char.isspace():
                        if len(currentString) > 0:
                            pastStrings.append(currentString)
                            currentString = ''
                    # Equals confirms that the parent node is case 3
                    elif char == '=':
                        name = None
                        if len(currentString) > 0:
                            name = currentString
                        else:
                            name = pastStrings[-1]
                        newNode = EU4DataNode(name)
                        dataPath[-1][name] = newNode
                        dataPath.append(newNode)
                        currentState = EU4DataFileReaderState.POST_EQUALS
                        pastStrings = []
                        currentString = ''
                    # Pop up a level. If there are leftover values, then the parent node is case 2
                    elif char == "}":
                        if len(pastStrings) > 0 or not currentString == '':
                            if len(currentString) > 0: 
                                pastStrings.append(currentString)
                            dataPath[-1].values = pastStrings
                            pastStrings = []
                            currentString = ''
                        dataPath.pop()
                    else:
                        currentString += char

                case EU4DataFileReaderState.POST_EQUALS:
                    if char.isspace():
                        pass
                    # Current node is Case 2 or 3
                    elif char == '{':
                        currentState = EU4DataFileReaderState.FIRST_STRING
                    # Current node is Case 1
                    elif char == "\"":
                        currentState = EU4DataFileReaderState.IN_QUOTATIONS
                        currentString += char
                    else:
                        currentState = EU4DataFileReaderState.SECOND_STRING
                        currentString += char

                case EU4DataFileReaderState.SECOND_STRING:
                    if char.isspace():
                        dataPath[-1].values = currentString
                        currentString = ''
                        dataPath.pop()
                        currentState = EU4DataFileReaderState.FIRST_STRING
                    else:
                        currentString += char

                case EU4DataFileReaderState.IN_QUOTATIONS:
                    currentString += char
                    if char == "\"":
                        dataPath[-1].values = currentString
                        currentString = ''
                        dataPath.pop()
                        currentState = EU4DataFileReaderState.FIRST_STRING
    return baseNode

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
    f = open(path, 'r', encoding="utf-8-sig", errors="ignore")
    r = ""
    for line in f.readlines():
        r += line.split('#')[0].strip() + ' '
    return r

# Test
if __name__ == "__main__":
    fileName = "E:/EU4Copy/common/country_tags/00_countries.txt"
    headNode = parseEU4File(fileName)
    print(headNode.values)
    writeToFileFromRootNode("C:/Users/User/Desktop/FileParserOutput.txt", headNode)