from enum import Enum
from os.path import exists
from os import listdir
from FileParser.EU4DataNode import EU4DataNode

# Three Cases:
# 1. key = value
# 2. key = { values ... values }
# 3. key = { key = ... key = ... }

class EU4DataFileState(Enum):
    STARTING_STATE = 1
    POST_FIRST_STRING = 2
    STRING_COLLECTION = 3
    POST_EQUALS = 4

class EU4DataFileTokenizerState(Enum):
    DEFAULT = 1
    IN_QUOTATIONS = 2
    IN_COMMENT = 3

def writeToFileFromRootNode(filePath, rootNode, fileEncoding):
    f = open(filePath, 'w', encoding=fileEncoding)
    for value in rootNode.getChildren():
        f.write(value.toString() + '\n')

def parseEU4File(path):
    tokens = tokenizeEU4DataFile(path)
    pastString = ""
    currentState = EU4DataFileState.STARTING_STATE
    dataNodeTree = [EU4DataNode("__ROOT__")]
    for token in tokens:
        match currentState:
            case EU4DataFileState.STARTING_STATE:
                if token == '}':
                    dataNodeTree.pop(-1)
                elif token in ['=', '{']:
                    raiseParserException(path, token, currentState, dataNodeTree)
                else:
                    pastString = token
                    currentState = EU4DataFileState.POST_FIRST_STRING
            case EU4DataFileState.POST_FIRST_STRING:
                if token == '=':
                    newNode = EU4DataNode(pastString)
                    pastString = ""
                    dataNodeTree[-1].addChildNode(newNode)
                    dataNodeTree.append(newNode)
                    currentState = EU4DataFileState.POST_EQUALS 
                elif token == '}':
                    dataNodeTree[-1].makeIntoEmptyList()
                    dataNodeTree[-1].addStringValue(pastString)
                    dataNodeTree.pop(-1)
                    currentState = EU4DataFileState.STARTING_STATE
                elif token == '{':
                    raiseParserException(path, token, currentState, dataNodeTree)
                else:
                    dataNodeTree[-1].addStringValue(pastString)
                    dataNodeTree[-1].addStringValue(token)
                    currentState = EU4DataFileState.STRING_COLLECTION
            case EU4DataFileState.STRING_COLLECTION:
                if token == '}':
                    dataNodeTree.pop(-1)
                    currentState = EU4DataFileState.STARTING_STATE
                elif token in ['=', '{']:
                    raiseParserException(path, token, currentState, dataNodeTree)
                else:
                    dataNodeTree[-1].addStringValue(token)
            case EU4DataFileState.POST_EQUALS:
                if token == '{':
                    currentState = EU4DataFileState.STARTING_STATE
                elif token in ['=', '}']:
                    raiseParserException(path, token, currentState, dataNodeTree)
                else:
                    dataNodeTree[-1].addStringValue(token)
                    dataNodeTree.pop(-1)
                    currentState = EU4DataFileState.STARTING_STATE
    return dataNodeTree.pop(0)

def parseEU4Folder(path):
    trees = []
    if exists(path):
        for fileName in listdir(path):
            fileName = "{}/{}".format(path, fileName)
            trees.append(parseEU4File(fileName))
    return trees

def raiseParserException(path, token, currentState, dataNodeTree):
    dataNodeTreePath = ""
    for i in range(0, len(dataNodeTree)):
        dataNodeTreePath += dataNodeTree[i].name
        if i != (len(dataNodeTree)-1):
            dataNodeTreePath += " --> "
    raise RuntimeError("Error while parsing file {}: Unexpected Token '{}' while in state {}! Current tree location: {}".format(path, token, currentState, dataNodeTreePath))

def tokenizeEU4DataFile(path):
    tokens = []
    currentState = EU4DataFileTokenizerState.DEFAULT
    currentString = ""
    if exists(path):
        for char in open(path, 'r', encoding="utf-8-sig", errors="ignore").read():
            match currentState:
                case EU4DataFileTokenizerState.DEFAULT:
                    if char.isspace():
                        if len(currentString) > 0:
                            tokens.append(currentString)
                            currentString = ""
                    elif char in ['=', '{', '}']:
                        if len(currentString) > 0:
                            tokens.append(currentString)
                            currentString = ""
                        tokens.append(char)
                    elif char == '\"':
                        if len(currentString) > 0:
                            tokens.append(currentString)
                            currentString = ""
                        currentState = EU4DataFileTokenizerState.IN_QUOTATIONS
                    elif char == '#':
                        if len(currentString) > 0:
                            tokens.append(currentString)
                            currentString = ""
                        currentState = EU4DataFileTokenizerState.IN_COMMENT
                    else:
                        currentString += char
                case EU4DataFileTokenizerState.IN_COMMENT:
                    if char == '\n':
                        currentState = EU4DataFileTokenizerState.DEFAULT
                case EU4DataFileTokenizerState.IN_QUOTATIONS:
                    if char == '\"':
                        tokens.append(currentString)
                        currentString = ""
                        currentState = EU4DataFileTokenizerState.DEFAULT
                    else:
                        currentString += char
    if len(currentString) > 0:
        tokens.append(currentString)
    return tokens