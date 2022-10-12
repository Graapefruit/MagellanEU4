# TODO: Monarchs/History
class Country:
    def __init__(self, tag):
        self.tag = tag
        self.name = ""
        self.adj = ""
        self.graphicalCulture = ""
        self.mapColor = None
        self.revolutionaryColors = ""
        self.historicalIdeas = ""
        self.historicalUnits = ""
        self.monarchNames = ""
        self.leaderNames = ""
        self.shipNames = ""
        self.armyNames = ""
        self.fleetNames = ""
        self.governmentType = ""
        self.governmentReforms = ""
        self.governmentRank = ""
        self.mercantilism = ""
        self.techGroup = ""
        self.religion = ""
        self.primaryCulture = ""
        self.acceptedCultures = ""
        self.capital = ""
        self.fixedCapital = ""
        self.color1 = None
        self.color2 = None
        self.color3 = None

    def populateFromCountryFileDataTree(self, dataTree):
        self.graphicalCulture = writeIfExist(dataTree, "graphical_culture")
        self.mapColor = writeColorIfExist(dataTree, "color")
        self.revolutionaryColors = writeIfExist(dataTree, "revolutionary_color")
        self.historicalIdeas = writeIfExist(dataTree, "historical_idea_groups")
        self.historicalUnits = writeIfExist(dataTree, "historical_units")
        self.monarchNames = writeIfExist(dataTree, "monarch_names")
        self.leaderNames = writeIfExist(dataTree, "leader_names")
        self.shipNames = writeIfExist(dataTree, "ship_names")
        self.armyNames = writeIfExist(dataTree, "army_names")
        self.fleetNames = writeIfExist(dataTree, "fleet_names")

    def populateFromHistoryFileDataTree(self, dataTree):
        self.governmentType = writeIfExist(dataTree, "government")
        self.governmentReforms = writeIfExist(dataTree, "add_government_reform")
        self.governmentRank = writeIfExist(dataTree, "government_rank")
        self.mercantilism = writeIfExist(dataTree, "mercantilism")
        self.techGroup = writeIfExist(dataTree, "technology_group")
        self.religion = writeIfExist(dataTree, "religion")
        self.primaryCulture = writeIfExist(dataTree, "primary_culture")
        self.acceptedCultures = writeIfExist(dataTree, "add_accepted_culture")
        self.capital = writeIfExist(dataTree, "capital")
        self.fixedCapital = writeIfExist(dataTree, "fixed_capital")

    def populateFromCountryColorsDataTree(self, dataTree):
        self.color1 = writeColorIfExist(dataTree, "color1")
        self.color2 = writeColorIfExist(dataTree, "color2")
        self.color3 = writeColorIfExist(dataTree, "color3")

def writeIfExist(dataNode, fieldName):
    return (dataNode[fieldName].values if fieldName in dataNode.values else "")

def writeColorIfExist(dataNode, fieldName):
    return ((dataNode[fieldName].values[0], dataNode[fieldName].values[1], dataNode[fieldName].values[2]) if fieldName in dataNode.values else None)