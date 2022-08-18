class EU4DataNode():
    def __init__(self, parent, string, depth):
        self.parent = parent
        self.values = dict()

        while string != "":
            equalsIndex = string.find('=')
            newlineIndex = string.find('\n')
            if equalsIndex == -1: # Case 2
                self.values = string.split()
                string = ""
            else:
                if '{' in string