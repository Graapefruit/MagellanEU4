from enum import Enum

class EU4DataNodeType(Enum):
    SINGLE_ENTRY = 1    # <key> = <value>
    LIST_ENTRY = 2      # <key> = { <value> <value> ... <value> }
    DUPLICATE_ENTRY = 3  # <key> = <value> ... <key> = <value>
    PARENT_NODE = 4     # <key> = { <key>, <key>, ..., <key> }

ERROR_STRING = "Error with EU4DataNode.{}: name: {}, type: {}, current value: {}, param: {}"
    
class EU4DataNode():
    def __init__(self, name):
        self.name = name
        self.type = None
        self.value = None

    def addStringValue(self, value):
        if self.type == None:
            self.type = EU4DataNodeType.SINGLE_ENTRY
            self.value = value
        elif self.type == EU4DataNodeType.SINGLE_ENTRY:
            self.type = EU4DataNodeType.LIST_ENTRY
            self.value = [self.value, value]
        elif self.type == EU4DataNodeType.LIST_ENTRY:
            self.value.append(value)
        else:
            print(ERROR_STRING.format("addStringValue", self.name, self.type, self.value, value))

    def addListValue(self, value):
        if self.type == None:
            self.type = EU4DataNodeType.LIST_ENTRY
            self.value = value
        elif self.type == EU4DataNodeType.SINGLE_ENTRY:
            self.type = EU4DataNodeType.LIST_ENTRY
            self.value = [self.value]
            self.value += value
        elif self.type == EU4DataNodeType.LIST_ENTRY:
            self.value += value
        else:
            print(ERROR_STRING.format("addListValuee", self.name, self.type, self.value, value))

    def addChildNode(self, value):
        if self.type == None:
            self.type = EU4DataNodeType.PARENT_NODE
            self.value = {value.name: value}
        elif self.type == EU4DataNodeType.PARENT_NODE:
            if value.name in self.value:
                if self.value[value.name] != EU4DataNodeType.DUPLICATE_ENTRY:
                    oldValue = self.value[value.name]
                    self.value[value.name] = EU4DataNode(self.name)
                    self.value[value.name].type = EU4DataNodeType.DUPLICATE_ENTRY
                    self.value[value.name].value = [oldValue]
                self.value[value.name].value.append(value)
            else:
                self.value[value.name] = value
        else:
            print(ERROR_STRING.format("addChildNode", self.name, self.type, self.value, value))

    def toString(self):
        return self._toStringHelper(0)

    def getChildren(self):
        if self.type == EU4DataNodeType.PARENT_NODE:
            return self.value.values()
        else:
            print("ERROR: getChildren called with unsupported type: {}".format(self.type))

    def getChildValue(self, childName):
        return self.value[childName].value

    def wipe(self):
        self.type = None
        self.value = None

    def getAndCreateIfNotExists(self, name):
        if self.type == None:
            self.type = EU4DataNodeType.PARENT_NODE
            self.value[name] = EU4DataNode(name)
        elif self.type == EU4DataNodeType.PARENT_NODE:
            if not name in self.value:
                self.value[name] = EU4DataNode(name)
        elif self.type == EU4DataNodeType.DUPLICATE_ENTRY:
            pass # We don't use this function for this case
        else:
            print("ERROR: getAndCreateIfNotExists called with unsupported type: {}".format(self.type))
        return self.value[name]

    def __getitem__(self, name):
        return self.value[name]

    def __setitem__(self, name, value):
        self.value[name] = value

    def __contains__(self, value):
        return value in self.value

    def _toStringHelper(self, depth):
        s = ""
        beginningString = "\t" * depth + self.name + " = "
        match self.type:
            case None:
                pass
            case EU4DataNodeType.SINGLE_ENTRY:
                s += beginningString + self.value + '\n'
            case EU4DataNodeType.LIST_ENTRY:
                s += beginningString + "{\n" + "\t" * (depth+1)
                for value in self.value:
                    s += value + ' '
                s += "\n" + "\t" * depth + "}\n"
            case EU4DataNodeType.PARENT_NODE:
                s += beginningString + "{\n"
                for child in self.value.values():
                    s += child._toStringHelper(depth+1)
                s += "\t" * depth + "}\n"
            case EU4DataNodeType.DUPLICATE_ENTRY:
                for duplicate in self.value:
                    s += duplicate._toStringHelper(depth)
            case _:
                print("WARNING: Values field of {}, {}, is of unrecognized type {}!".format(self.name, self.value, self.type))
        return s