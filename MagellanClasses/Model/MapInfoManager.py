from genericpath import isfile
from logging import root
import sys
import csv
from FileParser.EU4DataNode import EU4DataNodeType
from Utils.Country import Country
from Utils.Province import Province
from Utils.RGB import RGB
from MagellanClasses.Constants import *
from MagellanClasses.Defaults import *
from PIL import Image
from os import listdir, remove
from os.path import exists
import re
import numpy
from FileParser.EU4DataFileParser import *

class MapInfoManager():
    def __init__(self, path):
        self.path = path
        self.maxProvinces = 5000
        self.defaultsTree = EU4DataNode("__ROOT__")
        self.provinces = []
        self.areasToColors = dict()
        self.terrainTree = EU4DataNode("__ROOT__")
        self.tradeNodeTree = EU4DataNode("__ROOT__")
        self.techGroups = []
        self.colorsToProvinces = dict()
        self.religionsToColours = DEFAULT_RELIGIONS.copy()
        self.tradeGoodsToColours = dict()
        self.terrainsToColours = dict()
        self.tagsToColours = dict()
        self.tagNameDict = dict()
        self.rnwProvinces = set()
        self.cultures = []
        self.populateDefaults("{}/{}/{}".format(path, MAP_FOLDER_NAME, DEFAULTS_FILE_NAME))
        self.idsToProvinces = [None] * self.maxProvinces # Must grab the right maxProvinces from the Defaults file first
        self.populateTechGroups("{}/{}/{}".format(path, COMMON_FOLDER, TECHNOLOGY_FILE))
        self.populateFromDefinitionFile("{}/{}/{}".format(path, MAP_FOLDER_NAME, PROVINCE_DEFINITION_FILE_NAME))
        self.populateSeasAndLakes()
        self.populateProvinceHistoryFiles("{}/{}".format(path, PROVINCES_HISTORY_PATH))
        self.populateAreaData("{}/{}/{}".format(path, MAP_FOLDER_NAME, AREAS_FILE_NAME))
        self.populateProvinceTerrain("{}/{}/{}".format(path, MAP_FOLDER_NAME, TERRAIN_FILE_NAME))
        self.populateContinentData("{}/{}/{}".format(path, MAP_FOLDER_NAME, CONTINENTS_FILE_NAME))
        self.populateClimateData("{}/{}/{}".format(path, MAP_FOLDER_NAME, CLIMATE_FILE_NAME))
        self.populateNameData("{}/{}/{}".format(path, LOCALIZATION_FOLDER_NAME, LOCALIZATION_NAME_FILE))
        self.populateAdjectiveData("{}/{}/{}".format(path, LOCALIZATION_FOLDER_NAME, LOCALIZATION_NAME_FILE))
        self.populateTradeNodes("{}/{}/{}/{}".format(path, COMMON_FOLDER, TRADE_NODE_FOLDER, TRADE_NODES_FILE))
        self.populateReligionData("{}/{}/{}".format(path, COMMON_FOLDER, RELIGIONS_FOLDER))
        self.populateCultureData("{}/{}/{}".format(path, COMMON_FOLDER, CULTURES_FOLDER))
        self.provinceMapImage = Image.open("{}/{}/{}".format(path, MAP_FOLDER_NAME, PROVINCE_FILE_NAME))
        self.provinceMapArray = numpy.array(self.provinceMapImage)
        self.populateTradeGoodData("{}/{}/{}".format(path, COMMON_FOLDER, TRADE_GOODS_FOLDER))
        self.populateTags("{}/{}/{}".format(path, COMMON_FOLDER, TAGS_FOLDER))
        self.provinceMapLocation = "{}/{}/{}".format(path, MAP_FOLDER_NAME, PROVINCE_FILE_NAME)
        self.populatePixels()
        print("Finished Loading the Map Info")
        sys.stdout.flush()

    # --- Setup --- #

    def populateDefaults(self, path):
        print("Loading Defaults...")
        sys.stdout.flush()
        self.defaultsTree = parseEU4File(path)
        self.maxProvinces = int(self.defaultsTree.getChildValue("max_provinces"))

    def populateTechGroups(self, path):
        if exists(path):
            print("Parsing Tech Groups... ")
            sys.stdout.flush()
            rootNode = parseEU4File(path)
            for techGroupNode in rootNode["groups"].getChildren():
                self.techGroups.append(techGroupNode.name)
        else:
            self.techGroups = DEFAULT_TECH_GROUPS[:]
            print("{} could not be found. Will use base game tech groups instead")

    def populateFromDefinitionFile(self, path):
        print("Parsing Definition File... ")
        sys.stdout.flush()
        provincesInfo = open(path, 'r', errors="replace")
        reader = csv.reader(provincesInfo, delimiter=';')
        for provinceInfo in reader:
            if not provinceInfo[0].isdigit():
                continue
            rgb = (int(provinceInfo[1]), int(provinceInfo[2]), int(provinceInfo[3]))
            if (provinceInfo[4] == RNW_PROVINCE_KEY):
                self.rnwProvinces.add(int(provinceInfo[0]))
            else:
                if (rgb in self.colorsToProvinces):
                    print("ERROR: Two provinces share the same colour! IDs: {} {}".format(self.colorsToProvinces[rgb].id, provinceInfo[0]))
                    quit()
                self.createNewProvince(int(provinceInfo[0]), provinceInfo[4], rgb)

    def createNewProvince(self, id, name, rgb):
        province = Province(id, name, rgb)
        baseDiscovered = dict()
        for techGroup in self.techGroups:
            baseDiscovered[techGroup] = False
        province.discovered = baseDiscovered.copy()
        self.provinces.append(province)
        self.colorsToProvinces[rgb] = province
        self.idsToProvinces[id] = province
        return province

    def populateSeasAndLakes(self):
        for provinceId in self.defaultsTree.getChildValue("sea_starts"):
            provinceId = int(provinceId)
            if self.idsToProvinces[provinceId]:
                self.idsToProvinces[provinceId].isSea = True
        for provinceId in self.defaultsTree.getChildValue("lakes"):
            provinceId = int(provinceId)
            if self.idsToProvinces[provinceId]:
                self.idsToProvinces[provinceId].isLake = True
        self.defaultsTree["sea_starts"].wipe()
        self.defaultsTree["lakes"].wipe()

    def populateProvinceHistoryFiles(self, path):
        print("Parsing History Files...")
        sys.stdout.flush()
        provinceHistoryFiles = listdir(path)
        for fileName in provinceHistoryFiles:
            fileId = fileName.split("-")[0].split()[0]
            if fileId.isdigit() and self.idsToProvinces[int(fileId)] != None:
                province = self.idsToProvinces[int(fileId)]
                province.historyFile = fileName
                provinceTree = parseEU4File("{}/{}".format(path, fileName))
                if provinceTree.type == EU4DataNodeType.PARENT_NODE:
                    for field in provinceTree.getChildren():
                        lineKey = field.name.lower().strip().replace("\"", "")
                        if PROVINCE_DATE_UPDATE_PATTERN.match(lineKey):
                            province.provinceUpdates.append(field)
                        elif field.type == EU4DataNodeType.SINGLE_ENTRY:
                            lineVal = field.value.lower().strip().replace("\"", "")
                            match lineKey:
                                case "add_core":
                                    province.cores.append(lineVal)
                                case "owner":
                                    province.owner = lineVal
                                case "controller":
                                    province.controller = lineVal
                                case "culture":
                                    province.culture = lineVal
                                case "religion":
                                    province.religion = lineVal
                                case "hre":
                                    province.hre = True if lineVal.lower() == "yes" else False
                                case "base_tax":
                                    if lineVal.isdigit():
                                        province.tax = int(lineVal)
                                case "base_production":
                                    if lineVal.isdigit():
                                        province.production = int(lineVal)
                                case "base_manpower":
                                    if lineVal.isdigit():
                                        province.manpower = int(lineVal)
                                case "trade_goods":
                                    province.tradeGood = lineVal
                                case "discovered_by":
                                    province.discovered[lineVal] = True
                                case "capital":
                                    province.capital = field.value.strip().replace("\"", "")
                                case _:
                                    province.extraText += field.toString()
                        else:
                            province.extraText += field.toString()

    def populateAreaData(self, path):
        print("Populating Areas...")
        sys.stdout.flush()
        if exists(path):
            areaFile = open(path, 'r', errors="replace")
            fileWithoutComments = ""
            for line in areaFile:
                fileWithoutComments += line.split('#')[0] + '\n'
            matches = re.findall(AREA_GROUPING_PATTERN, fileWithoutComments)
            for match in matches:
                name = match[0]
                color = None
                if match[1]:
                    rgbComponents = re.findall(AREA_COLOR_GROUPING_PATTERN, match[1])[0]
                    color = RGB(rgbComponents[0], rgbComponents[1], rgbComponents[2])
                for province in match[2].split():
                    if province.isnumeric():
                        self.idsToProvinces[int(province)].area = name
                self.areasToColors[name] = color
        else:
            print("No Area File Found")
            sys.stdout.flush()

    def populateProvinceTerrain(self, path):
        print("Parsing Terrains...")
        sys.stdout.flush()
        if exists(path):
            rootNode = parseEU4File(path)
            self.terrainTree = rootNode
            for category in rootNode["categories"].getChildren():
                if "terrain_override" in category:
                    for provinceIdString in category.getChildValue("terrain_override"):
                        provinceId = int(provinceIdString)
                        if provinceId < len(self.idsToProvinces) and self.idsToProvinces[provinceId] != None:
                            self.idsToProvinces[provinceId].terrain = category.name
                    category["terrain_override"].wipe()
                if "color" in category:
                    colorString = category.getChildValue("color")
                    self.terrainsToColours[category.name] = (int(colorString[0]), int(colorString[1]), int(colorString[2]))
            
    def populateContinentData(self, path):
        print("Parsing Continents...")
        sys.stdout.flush()
        if exists(path):
            continentsFile = open(path, 'r', errors="replace")
            matches = re.findall(CONTINENT_FILE_GROUPING_PATTERN, continentsFile.read())
            for match in matches:
                continentName = match[0]
                for line in match[1].split("\n"):
                    provinceIds = line.split('#')[0].split()
                    for provinceId in provinceIds:
                        if provinceId.isdigit() and self.idsToProvinces[int(provinceId)]:
                            self.idsToProvinces[int(provinceId)].continent = continentName
        else:
            print("No Continents File Found")
            sys.stdout.flush()

    def populateClimateData(self, path):
        print("Parsing {}...".format(CLIMATE_FILE_NAME))
        sys.stdout.flush()
        if exists(path):
            climateFileText = self.getFileTextWithoutComments(path)
            matches = re.findall(CLIMATE_FILE_GROUPING_PATTERN, climateFileText)
            for match in matches:
                key = match[0]
                values = match[1].split()
                for value in values:
                    if value.isdigit() and self.idsToProvinces[int(value)] != None:
                        if key in DEFAULT_CLIMATES:
                            self.idsToProvinces[int(value)].climate = key
                        elif key in DEFAULT_WEATHERS:
                            self.idsToProvinces[int(value)].weather = key
                        elif key == "impassable":
                            self.idsToProvinces[int(value)].impassable = True
        else:
            print("No Climate File Found")
            sys.stdout.flush()

    def populateNameData(self, path):
        print("Parsing {}...".format(LOCALIZATION_NAME_FILE))
        sys.stdout.flush()
        if exists(path):
            nameFileText = self.getFileTextWithoutComments(path)
            matches = re.findall(LOCALIZATION_NAME_PATTERN, nameFileText)
            for match in matches:
                provinceId = int(match[0])
                provinceName = match[1]
                self.idsToProvinces[provinceId].localizationName = provinceName
        else:
            print("{} not found".format(LOCALIZATION_NAME_FILE))
            sys.stdout.flush()

    def populateAdjectiveData(self, path):
        print("Parsing {}...".format(LOCALIZATION_ADJECTIVE_FILE))
        sys.stdout.flush()
        if exists(path):
            nameFileText = self.getFileTextWithoutComments(path)
            matches = re.findall(LOCALIZATION_ADJECTIVE_PATTERN, nameFileText)
            for match in matches:
                provinceId = int(match[0])
                provinceAdjective = match[1]
                self.idsToProvinces[provinceId].localizationAdjective = provinceAdjective
        else:
            print("{} not found".format(LOCALIZATION_ADJECTIVE_FILE))
            sys.stdout.flush()

    def populateTradeNodes(self, path):
        if exists(path):
            tradeNodeTree = parseEU4File(path)
            if self.tradeNodeTree.getChildren() != None:
                print("Parsing Trade Nodes...")
                sys.stdout.flush()
                self.tradeNodeTree = tradeNodeTree
                for tradeNode in self.tradeNodeTree.getChildren():
                    if "members" in tradeNode:
                        for provinceId in tradeNode.getChildValue("members"):
                            if provinceId.isdigit() and int(provinceId) < len(self.idsToProvinces) and self.idsToProvinces[int(provinceId)] != None:
                                self.idsToProvinces[int(provinceId)].tradeNode = tradeNode.name
                        tradeNode["members"].wipe()
            else:
                print("NOTE: Empty trade node file found!")
                sys.stdout.flush()
        else:
            print("NOTE: No trade node file found!")
            sys.stdout.flush()

    def populatePixels(self):
        newProvinceIndex = 1
        print("Populating Pixels... This may take a while")
        sys.stdout.flush()
        for y in range(0, len(self.provinceMapArray)):
            for x in range(0, len(self.provinceMapArray[y])):
                province = self.getProvinceAtIndex(x, y)
                # Create new Province
                if province == None:
                    while newProvinceIndex < self.maxProvinces:
                        if newProvinceIndex not in self.rnwProvinces and self.idsToProvinces[newProvinceIndex] == None:
                            province = self.createNewProvince(newProvinceIndex, "newProvince{}".format(newProvinceIndex), self.getColourAtIndex(x, y))
                            province.historyFile = "{} - {}.txt".format(province.id, province.name)
                            break
                        newProvinceIndex += 1
                    if newProvinceIndex == self.maxProvinces:
                        sys.exit("ERROR: Needed to create a new province for color {}, but hit the max province ID {}. Please increase your max province count!".format())
                province.pixels.append((x, y))
                    

        for province in self.idsToProvinces:
            if province:
                province.pixels = numpy.array(province.pixels)

    def populateReligionData(self, path):
        if exists(path):
            print("Poulating Religion -> Colour mappings...")
            sys.stdout.flush()
            # If the base file exists, we overwrite base game values. Otherwise, we include them
            if exists("{}/{}".format(path, RELIGIONS_FILE)):
                self.religionsToColours = dict()
            for fileName in listdir(path):
                filePath = "{}/{}".format(path, fileName)
                rootNode = parseEU4File(filePath)
                for religionGroup in rootNode.getChildren():
                    # Parse through every field in a religious group. Religions are every child that is a data node and isn't a muslim religious school
                    for religionGroupData in religionGroup.getChildren():
                        if religionGroupData.type == EU4DataNodeType.PARENT_NODE and religionGroupData.name != "religious_schools":
                            religionName = religionGroupData.name
                            religionColour = religionGroupData["color"]
                            religionColour = (int(religionColour[0]), int(religionColour[1]), int(religionColour[2]))
                            self.religionsToColours[religionName] = religionColour
        else:
            print("NOTE: Could not find religions folder path. The religions mapmode will have default colours.")

    def populateCultureData(self, path):
        if exists(path):
            print("Populating Cultures...")
            sys.stdout.flush()
            for fileName in listdir(path):
                filePath = "{}/{}".format(path, fileName)
                rootNode = parseEU4File(filePath)
                for cultureGroup in rootNode.getChildren():
                    for culture in cultureGroup.getChildren():
                        if culture.name not in ["graphical_culture", "second_graphical_culture", "male_names", "female_names", "dynasty_names"]:
                            self.cultures.append(culture.name)
        else:
            print("NOTE: Could not find cultures folder path. They will not be auto-populated.")

    def populateTradeGoodData(self, path):
        if exists(path):
            print("Poulating Trade Good -> Colour mappings...")
            sys.stdout.flush()
            for fileName in listdir(path):
                filePath = "{}/{}".format(path, fileName)
                rootNode = parseEU4File(filePath)
                for tradeGood in rootNode.getChildren():
                    tradeGoodColour = tradeGood["color"]
                    self.tradeGoodsToColours[tradeGood.name] = (round(float(tradeGoodColour[0]) * 255), round(float(tradeGoodColour[1]) * 255), round(float(tradeGoodColour[2]) * 255))
        else:
            print("NOTE: Could not find tradegoods folder path. The tradegoods mapmode will have random colours.")

    def populateTags(self, tagsPath):
        if exists(tagsPath):
            print("Poulating Tags...")
            sys.stdout.flush()
            for tagFile in listdir(tagsPath):
                filePath = "{}/{}".format(tagsPath, tagFile)
                rootNode = parseEU4File(filePath)
                for tag in rootNode.getChildren():
                    tagName = tag.name.lower()
                    self.tagNameDict[tagName] = Country(tagName)
                    # country file
                    countryInternalName = tag.value
                    countryFilePath = "{}/{}/{}".format(self.path, COMMON_FOLDER, countryInternalName)
                    if exists(countryFilePath):
                        tagData = parseEU4File(countryFilePath)
                        colorList = tagData.getChildValue("color")
                        color = (int(colorList[0]), int(colorList[1]), int(colorList[2]))
                        self.tagsToColours[tagName] = color
                        self.tagNameDict[tagName].populateFromCountryFileDataTree(tagData)
                    else:
                        print("Tag {} defined, but no corresponding country file found. Skipping...".format(countryInternalName))
                # history file
                historyFilesPath = "{}/{}".format(self.path, COUNTRIES_HISTORY_PATH)
                if exists(historyFilesPath):
                    for historyFile in listdir(historyFilesPath):
                        tag = historyFile.split('-')[0].strip().lower()
                        if tag in self.tagNameDict:
                            tagData = parseEU4File("{}/{}".format(historyFilesPath, historyFile))
                            self.tagNameDict[tag].populateFromHistoryFileDataTree(tagData)
                        else:
                            print("Warning: found history file with no existing tag: \"{}\". Will be skipped".format(historyFile))
                else:
                    print("Could not find the history file path for countries. Skipping...")
                # localization
                countryLocalizationPath = "{}/{}/{}".format(self.path, LOCALIZATION_FOLDER_NAME, COUNTRIES_LOCALIZATION_FILE)
                if exists(countryLocalizationPath):
                    for match in re.findall(COUNTRY_LOCALIZATION_PATTERN, open(countryLocalizationPath, 'r').read()):
                        tag = match[0].strip().lower()
                        if tag in self.tagNameDict:
                            country = self.tagNameDict[tag]
                            localizationString = match[2]
                            print(localizationString)
                            if match[1] == "_ADJ":
                                country.adj = localizationString
                            else:
                                country.name = localizationString
                        else:
                            print("Warning: line found in localization with no corresponding tag: {}".format(match[0]))
                else:
                    print("Could not find the localization file for the countries. Skipping...")
                # colours
                countryColoursPath = "{}/{}".format(self.path, COUNTRY_COLORS_FOLDER)
                if exists(countryColoursPath):
                    for countryColourFile in listdir(countryColoursPath):
                        for countryColour in parseEU4File(countryColourFile).getChildren():
                            tag = countryColour.name.strip().lower()
                            if tag in self.tagNameDict:
                                self.tagNameDict[tag].populateFromCountryColorsDataTree(countryColour)
                            else:
                                print("Entry {} exists in {}, but no corresponding tag exists!".format(tag, countryColourFile))
                else:
                    print("Could not find the path for country colours. Skipping...")
        else:
            print("NOTE: Could not find {}. Tags will not be loaded.".format(tagsPath))

    # --- Utility --- #

    def getFileTextWithoutComments(self, path):
        f = open(path, 'r', encoding="utf-8-sig", errors="replace")
        fileText = ""
        for line in f:
            commentPartitions = line.split('#')
            fileText += line.split('#')[0]
            if len(commentPartitions) > 1:
                fileText += "\n"
        return fileText

    def getColourAtIndex(self, x, y):
        return (self.provinceMapArray[y][x][0], self.provinceMapArray[y][x][1], self.provinceMapArray[y][x][2]) 

    def getProvinceAtIndex(self, x, y):
        return self.colorsToProvinces.get(self.getColourAtIndex(x, y))

    # --- Public --- #

    def generatePositions(self):
        print("Generating Positions...")
        sys.stdout.flush()
        root = EU4DataNode("__ROOT__")
        path = "{}/{}/{}".format(self.path, MAP_FOLDER_NAME, POSITIONS_FILE_NAME)
        idsToSkip = set()
        if exists(path):
            root = parseEU4File(path)
            for province in root.getChildren():
                idsToSkip.add(int(province.name))
        for province in self.idsToProvinces:
            if province != None and province.id not in idsToSkip and len(province.pixels) > 0:
                avaeragePos = numpy.average(province.pixels, axis=0)
                x = "{:.3f}".format(round(avaeragePos[0], 4))
                y = "{:.3f}".format(round(avaeragePos[1], 4))
                newNode = EU4DataNode(str(province.id))
                positionNode = EU4DataNode("position")
                positionNode.addListValue(x, y, x, y, x, y, x, y, x, y, x, y, x, y)
                newNode.addChildNode(positionNode)

                rotationNode = EU4DataNode("rotation")
                rotationNode.addListValue("0.000", "0.000", "0.000", "0.000", "0.000", "0.000", "0.000")
                newNode.addChildNode(rotationNode)

                heightNode = EU4DataNode("height")
                heightNode.addListValue("0.000", "0.000", "0.000", "0.000", "0.000", "0.000", "0.000")
                newNode.addChildNode(heightNode)
                root.addChildNode(newNode)
        writeToFileFromRootNode(path, root)
        print("Done.")
        sys.stdout.flush()

    def propagateOwnerData(self):
        print("Propagating Owner Data...")
        sys.stdout.flush()
        modifiedProvinces = set()
        for province in self.idsToProvinces:
            if province != None and province.owner != "":
                if province.controller == "":
                    province.controller = province.owner
                    modifiedProvinces.add(province)
                if len(province.cores) == 0:
                    province.cores.append(province.owner)
                    modifiedProvinces.add(province)
        print("Done.")
        sys.stdout.flush()
        return modifiedProvinces

    def clearAllProvinceHistoryUpdates(self):
        print("Clearing all Province History Updates...")
        sys.stdout.flush()
        modifiedProvinces = set()
        for province in self.idsToProvinces:
            if province != None and len(province.provinceUpdates) > 0:
                province.provinceUpdates = []
                modifiedProvinces.add(province)
        print("Done.")
        sys.stdout.flush()
        return modifiedProvinces

    def updateProvinceHistoryFileNames(self):
        print("Updaing Province History File names")
        sys.stdout.flush()
        for province in self.provinces:
            newFileName = "{} - {}.txt".format(province.id, province.name)
            newFilePath = "{}/{}/{}".format(self.path, PROVINCES_HISTORY_PATH, newFileName)
            if not exists(newFilePath):
                oldFilePath = "{}/{}/{}".format(self.path, PROVINCES_HISTORY_PATH, province.historyFile)
                fileContents = open(oldFilePath, 'r').read()
                open(newFilePath, "w+").write(fileContents)
                remove(oldFilePath)
                province.historyFile = newFileName
        print("Done")
        sys.stdout.flush()

    def save(self, updatedProvinces):
        areasToProvinces = dict()
        continentsToProvinces = dict()
        climateEntryToProvinces = dict()
        climateEntryToProvinces["impassable"] = []

        for climate in DEFAULT_CLIMATES:
            if climate != "":
                climateEntryToProvinces[climate] = []
        for weather in DEFAULT_WEATHERS:
            if weather != "":
                climateEntryToProvinces[weather] = []
        for tradeNode in self.tradeNodeTree.getChildren():
            if "members" in tradeNode:
                tradeNode["members"].value = dict()
        for province in self.provinces:
            if province.area != "":
                if province.area in areasToProvinces:
                    areasToProvinces[province.area].append(province.id)
                else:
                    areasToProvinces[province.area] = [province.id]
            if province.terrain != "":
                self.terrainTree["categories"].getAndCreateIfNotExists(province.terrain).getAndCreateIfNotExists("terrain_override").addStringValue(str(province.id))
            if province.continent != "":
                if province.continent in continentsToProvinces:
                    continentsToProvinces[province.continent].append(province.id)
                else:
                    continentsToProvinces[province.continent] = [province.id]
            if province.climate != "":
                climateEntryToProvinces[province.climate].append(province.id)
            if province.weather != "":
                climateEntryToProvinces[province.weather].append(province.id)
            if province.impassable:
                climateEntryToProvinces["impassable"].append(province.id)
            if province.tradeNode != "" and not province.tradeNode.isspace():
                self.tradeNodeTree.getAndCreateIfNotExists(province.tradeNode).getAndCreateIfNotExists("members").addStringValue(str(province.id))
            if province.isSea:
                self.defaultsTree["sea_starts"].addStringValue(str(province.id))
            if province.isLake:
                self.defaultsTree["lakes"].addStringValue(str(province.id))

        
        print("Saving History Files...")
        sys.stdout.flush()
        for province in updatedProvinces:
            saveFileSafely("{}/{}/{}".format(self.path, PROVINCES_HISTORY_PATH, province.historyFile), (lambda : self.saveProvinceHistory(province)))

        saveFileSafely("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, PROVINCE_DEFINITION_FILE_NAME), (lambda : self.saveProvinceDefinitions()))
        saveFileSafely("{}/{}/{}".format(self.path, LOCALIZATION_FOLDER_NAME, LOCALIZATION_NAME_FILE), (lambda : self.saveLocalization(LOCALIZATION_NAME_FILE, "Name", "PROV")))
        saveFileSafely("{}/{}/{}".format(self.path, LOCALIZATION_FOLDER_NAME, LOCALIZATION_ADJECTIVE_FILE), (lambda : self.saveLocalization(LOCALIZATION_ADJECTIVE_FILE, "Adjective", "ADJ")))
        saveFileSafely("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, AREAS_FILE_NAME), (lambda : self.saveAreaFile(areasToProvinces)))
        saveFileSafely("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, TERRAIN_FILE_NAME), (lambda : self.saveDataTree("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, TERRAIN_FILE_NAME), "Terrain", self.terrainTree)))
        saveFileSafely("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, CONTINENTS_FILE_NAME), lambda : self.saveContinentsFile(continentsToProvinces))
        saveFileSafely("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, CLIMATE_FILE_NAME), (lambda : self.saveClimateFile(climateEntryToProvinces)))
        saveFileSafely("{}/{}/{}/{}".format(self.path, COMMON_FOLDER, TRADE_NODE_FOLDER, TRADE_NODES_FILE), (lambda : self.saveDataTree("{}/{}/{}/{}".format(self.path, COMMON_FOLDER, TRADE_NODE_FOLDER, TRADE_NODES_FILE), "Trade Node", self.tradeNodeTree)))
        saveFileSafely("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, DEFAULTS_FILE_NAME), (lambda : self.saveDataTree("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, DEFAULTS_FILE_NAME), "Defaults", self.defaultsTree)))
        print("Saving Success")
        sys.stdout.flush()

    def saveProvinceHistory(self, province):
        # None Previously
        if province.historyFile == "":
            province.historyFile = "{} - {}.txt".format(province.id, province.name)
        f = open("{}/{}/{}".format(self.path, PROVINCES_HISTORY_PATH, province.historyFile), 'w', encoding="ANSI")
        if isWalkableLand(province):
            writeFieldIfExists(f, "capital", "\"{}\"".format(province.capital))
            writeFieldIfExists(f, "owner", province.owner.upper())
            writeFieldIfExists(f, "controller", province.controller.upper())
            for core in province.cores:
                f.write("add_core = {}\n".format(core.upper()))
            writeFieldIfExists(f, "culture", province.culture)
            writeFieldIfExists(f, "religion", province.religion)
            f.write("hre = {}\n".format("yes" if province.hre else "no"))
            f.write("base_tax = {}\n".format(province.tax))
            f.write("base_production = {}\n".format(province.production))
            f.write("base_manpower = {}\n".format(province.manpower))
            writeFieldIfExists(f, "trade_goods", province.tradeGood)

        for discoverer in (techGroup for techGroup in province.discovered.keys() if province.discovered[techGroup]):
            f.write("discovered_by = {}\n".format(discoverer))
        f.write(province.extraText)

        for historyUpdate in province.provinceUpdates:
            f.write(historyUpdate.toString())
        f.close()
    
    def saveProvinceDefinitions(self):
        print("Saving Province Definitions...")
        sys.stdout.flush()
        f = open("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, PROVINCE_DEFINITION_FILE_NAME), 'w')
        f.write("province;red;green;blue;x;x\n")
        for province in self.idsToProvinces:
            if province != None:
                f.write("{};{};{};{};{};x\n".format(province.id, province.color[0], province.color[1], province.color[2], province.name))

    def saveLocalization(self, fileName, localizationType, localizationPrefix):
        print("Saving {} Localizations...".format(localizationType))
        sys.stdout.flush()
        f = open("{}/{}/{}".format(self.path, LOCALIZATION_FOLDER_NAME, fileName), 'w', encoding="utf-8-sig")
        f.write("l_english:\n")
        for province in self.idsToProvinces:
            if province != None:
                f.write(" {}{}:0 \"{}\"\n".format(localizationPrefix, province.id, province.localizationName))

    def saveAreaFile(self, areasToProvinces):
        print("Saving Area File...")
        sys.stdout.flush()
        f = open("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, AREAS_FILE_NAME), 'w')
        for area in areasToProvinces:
            f.write("{} = {{\n".format(area))
            if area in self.areasToColors and self.areasToColors[area]:
                color = self.areasToColors[area]
                f.write("\tcolor = {{ {} {} {} }}\n".format(color.red, color.green, color.blue))
            f.write("\t")
            for provinceId in areasToProvinces.get(area):
                f.write("{} ".format(provinceId))
            f.write("\n}\n\n")
        f.close()

    def saveDataTree(self, path, name, tree):
        print("Saving {} File...".format(name))
        sys.stdout.flush()
        writeToFileFromRootNode(path, tree)

    def saveContinentsFile(self, continentsToProvinces):
        print("Saving Continent File...")
        sys.stdout.flush()
        f = open("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, CONTINENTS_FILE_NAME), 'w')
        for continentName in continentsToProvinces:
            f.write("{} = {{\n\t".format(continentName))
            charactersOnLine = 0
            for provinceId in continentsToProvinces[continentName]:
                f.write("{} ".format(provinceId))
                charactersOnLine += len(str(provinceId)) + 1
                if charactersOnLine >= PROVINCE_CHARACTERS_PER_LINE:
                    f.write("\n\t")
                    charactersOnLine = 0
            f.write("\n}\n\n")
        f.close()

    def saveClimateFile(self, climateEntryToProvinces):
        print("Saving Climate/Weather File...")
        sys.stdout.flush()
        f = open("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, CLIMATE_FILE_NAME), 'w')
        for climateKey in climateEntryToProvinces:
            f.write("{} = {{\n\t".format(climateKey))
            charactersOnLine = 0
            for provinceId in climateEntryToProvinces[climateKey]:
                f.write("{} ".format(provinceId))
                charactersOnLine += len(str(provinceId)) + 1
                if charactersOnLine >= PROVINCE_CHARACTERS_PER_LINE:
                    f.write("\n\t")
                    charactersOnLine = 0
            f.write("\n}\n\n")
        f.write("equator_y_on_province_image = 656") # I have no clue what this does, but its always at the end of the climate.txt file so...
        f.close()

def isWalkableLand(province):
    return not (province.isSea or province.isLake or province.impassable)

def saveFileSafely(filePath, saveFunc):
    originalFileContents = None
    if exists(filePath) and isfile(filePath):
        originalFileContents = open(filePath, 'r', encoding="utf-8", errors="surrogateescape").read()
    try:
        saveFunc()
    except Exception as e:
        if exists(filePath):
            open(filePath, 'w', encoding="utf-8", errors="surrogateescape").write(originalFileContents)
            print("Something went wrong when saving to {}. The original file contents have been kept, and the rest of the files will be saved.\nError:\n{}".format(filePath, e))
        else:
            print("Something went wrong when saving to {}. The file did not exist before, so this step will have to be skipped.\nError:\n{}".format(filePath, e))

def writeFieldIfExists(file, text, field):
    if field != "":
        file.write("{} = {}\n".format(text, field))