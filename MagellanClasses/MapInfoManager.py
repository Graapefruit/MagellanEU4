import sys
import csv
from Utils.Province import Province
from Utils.ProvinceUpdate import ProvinceUpdate
from Utils.RGB import RGB
from MagellanClasses.Constants import *
from .Defaults import *
from PIL import Image
from os import listdir
from os.path import exists
import re
import numpy
from MagellanClasses.EU4DataFileParser import *

class MapInfoManager():
    def __init__(self, path):
        self.path = path
        self.max_provinces = 6500 # TODO: Grab this from Default.map
        self.provinces = []
        self.areasToColors = dict()
        self.terrainTree = EU4DataNode("__ROOT__")
        self.tradeNodeTree = EU4DataNode("__ROOT__")
        self.colorsToProvinces = dict()
        self.idsToProvinces = [None] * self.max_provinces
        self.populateFromDefinitionFile("{}/{}/{}".format(path, MAP_FOLDER_NAME, PROVINCE_DEFINITION_FILE_NAME))
        self.populateProvinceHistoryFiles("{}/{}".format(path, PROVINCES_HISTORY_PATH))
        self.populateAreaData("{}/{}/{}".format(path, MAP_FOLDER_NAME, AREAS_FILE_NAME))
        self.populateProvinceTerrain("{}/{}/{}".format(path, MAP_FOLDER_NAME, TERRAIN_FILE_NAME))
        self.populateContinentData("{}/{}/{}".format(path, MAP_FOLDER_NAME, CONTINENTS_FILE_NAME))
        self.populateClimateData("{}/{}/{}".format(path, MAP_FOLDER_NAME, CLIMATE_FILE_NAME))
        self.populateNameData("{}/{}/{}".format(path, LOCALIZATION_FOLDER_NAME, LOCALIZATION_NAME_FILE))
        self.populateAdjectiveData("{}/{}/{}".format(path, LOCALIZATION_FOLDER_NAME, LOCALIZATION_NAME_FILE))
        self.populateTradeNodes("{}/{}/{}/{}".format(path, COMMON_FOLDER, TRADE_NODE_FOLDER, TRADE_NODES_FILE))
        self.provinceMapImage = Image.open("{}/{}/{}".format(path, MAP_FOLDER_NAME, PROVINCE_FILE_NAME))
        self.provinceMapArray = numpy.array(self.provinceMapImage)
        # self.populatePixels()
        self.provinceMapLocation = "{}/{}/{}".format(path, MAP_FOLDER_NAME, PROVINCE_FILE_NAME)

    # --- Setup --- #

    def populateFromDefinitionFile(self, path):
        print("Parsing Definition File... ")
        sys.stdout.flush()
        provincesInfo = open(path)
        reader = csv.reader(provincesInfo, delimiter=';')
        for provinceInfo in reader:
            if not provinceInfo[0].isdigit():
                continue
            rgb = (int(provinceInfo[1]), int(provinceInfo[2]), int(provinceInfo[3]))
            # Skip RNW Provinces (some even share the same colors; yuck wtf)
            if (provinceInfo[4] == RNW_PROVINCE_KEY):
                continue
            if (rgb in self.colorsToProvinces):
                print("ERROR: Two provinces share the same colour! IDs: {} {}".format(self.colorsToProvinces[rgb].id, provinceInfo[0]))
                quit()
            province = Province(int(provinceInfo[0]), provinceInfo[4], rgb)
            self.provinces.append(province)
            self.colorsToProvinces[rgb] = province
            self.idsToProvinces[int(provinceInfo[0])] = province

    def populateProvinceHistoryFiles(self, path):
        print("Parsing History Files...")
        sys.stdout.flush()
        provinceHistoryFiles = listdir(path)
        for fileName in provinceHistoryFiles:
            fileId = fileName.split("-")[0].split()[0]
            if fileId.isdigit():
                province = self.idsToProvinces[int(fileId)]
                province.historyFile = fileName
                provinceHistoryText = open("{}/{}".format(path, fileName), 'r').read()
                provinceHistoryUpdates = re.findall(PROVINCE_DATE_UPDATE_GROUPING_PATTERN, provinceHistoryText)
                for match in provinceHistoryUpdates:
                    year, month, day = match[0].strip().split('.')
                    text = match[1]
                    province.provinceUpdates.append(ProvinceUpdate(int(year), int(month), int(day), text))
                HistoryUpdatesToRemove = re.findall(PROVINCE_DATE_UPDATE_PATTERN, provinceHistoryText)
                for match in HistoryUpdatesToRemove:
                    provinceHistoryText = provinceHistoryText.replace(match, '')
                for line in provinceHistoryText.split('\n'):
                    splitLine = line.split("=")
                    if len(splitLine) == 2:
                        lineKey = splitLine[0].lower().strip()
                        lineVal = splitLine[1].lower().strip()
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
                                province.hre = True if "yes" else False
                            case "base_tax":
                                province.tax = lineVal
                            case "base_production":
                                province.production = lineVal
                            case "base_manpower":
                                province.manpower = lineVal
                            case "trade_good":
                                province.tradeGood = lineVal
                            case "discovered_by":
                                province.discovered.append(lineVal)
                            case "capital":
                                province.capital = lineVal.replace('\"', '')
                            case _:
                                province.extraText += line.strip() + '\n'

    def populateAreaData(self, path):
        print("Populating Areas...")
        sys.stdout.flush()
        if exists(path):
            areaFile = open(path, 'r')
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
                    for provinceIdString in category["terrain_override"].values:
                        provinceId = int(provinceIdString)
                        if provinceId < len(self.idsToProvinces) and self.idsToProvinces[provinceId] != None:
                            self.idsToProvinces[provinceId].terrain = category.name
                    category["terrain_override"].values = []
            
    def populateContinentData(self, path):
        print("Parsing Continents...")
        sys.stdout.flush()
        if exists(path):
            continentsFile = open(path, 'r')
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
        print("Parsing Trade Nodes...")
        sys.stdout.flush()
        if exists(path):
            rootNode = parseEU4File(path)
            self.tradeNodeTree = rootNode
            for tradeNode in rootNode.getChildren():
                if "members" in tradeNode:
                    for provinceId in tradeNode["members"].values:
                        if provinceId.isdigit() and int(provinceId) < len(self.idsToProvinces) and self.idsToProvinces[int(provinceId)] != None:
                            self.idsToProvinces[int(provinceId)].tradeNode = tradeNode.name
                    tradeNode["members"].values = []

    def populatePixels(self):
        #TODO: Slow-ish. Multithread?
        print("Populating Pixels... This may take a while")
        sys.stdout.flush()
        for y in range(0, len(self.provinceMapArray)):
            for x in range(0, len(self.provinceMapArray[y])):
                self.getProvinceAtIndex(x, y).pixels.append((x, y))

    # --- Utility --- #

    def getFileTextWithoutComments(self, path):
        f = open(path, 'r', encoding="utf-8-sig")
        fileText = ""
        for line in f:
            fileText += line.split('#')[0]
        return fileText

    # --- Public --- #

    def getProvinceAtIndex(self, x, y):
        province = self.colorsToProvinces.get((self.provinceMapArray[y][x][0], self.provinceMapArray[y][x][1], self.provinceMapArray[y][x][2]))
        return province
    #def generateReligionMap(self):

    def save(self, updatedProvinces):
        areasToProvinces = dict()
        continentsToProvinces = dict()
        climateEntryToProvinces = dict()
        climateEntryToProvinces["impassable"] = []

        for climate in DEFAULT_CLIMATES:
            climateEntryToProvinces[climate] = []
        for weather in DEFAULT_WEATHERS:
            climateEntryToProvinces[weather] = []
        for province in self.provinces:
            if province.area != "":
                if province.area in areasToProvinces:
                    areasToProvinces[province.area].append(province.id)
                else:
                    areasToProvinces[province.area] = [province.id]
            if province.terrain != "":
                self.terrainTree["categories"].getAndCreateIfNotExists(province.terrain).getAndCreateIfNotExists("terrain_override").appendValueOverwriteDict(str(province.id))
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
                self.tradeNodeTree.getAndCreateIfNotExists(province.tradeNode).getAndCreateIfNotExists("members").appendValueOverwriteDict(str(province.id))
        
        print("Saving History Files...")
        sys.stdout.flush()
        for province in updatedProvinces:
            f = open("{}/{}/{}".format(self.path, PROVINCES_HISTORY_PATH, province.historyFile), 'w')
            if not self.provinceIsWater(province):
                writeFieldIfExists(f, "capital", province.capital)
                writeFieldIfExists(f, "owner", province.owner)
                writeFieldIfExists(f, "controller", province.controller)
                for core in province.cores:
                    f.write("add_core = {}\n".format(core))
                writeFieldIfExists(f, "culture", province.culture)
                writeFieldIfExists(f, "religion", province.religion)
                f.write("hre = {}\n".format("yes" if province.hre else "no"))
                f.write("base_tax = {}\n".format(province.tax))
                f.write("base_production = {}\n".format(province.production))
                f.write("base_manpower = {}\n".format(province.manpower))
                writeFieldIfExists(f, "trade_good", province.tradeGood)

            for discoverer in province.discovered:
                f.write("discovered_by = {}\n".format(discoverer))
            f.write(province.extraText)

            for historyUpdate in province.provinceUpdates:
                f.write("{} = {{{}}}".format(historyUpdate.date.strftime("%Y.%m.%d"), historyUpdate.text))
            f.close()

        print("Saving Province Definitions...")
        sys.stdout.flush()
        f = open("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, PROVINCE_DEFINITION_FILE_NAME), 'w')
        f.write("province;red;green;blue;x;x\n")
        for province in self.idsToProvinces:
            if province != None:
                f.write("{};{};{};{};{};x\n".format(province.id, province.color[0], province.color[1], province.color[2], province.name))

        print("Saving Name Localizations...")
        sys.stdout.flush()
        f = open("{}/{}/{}".format(self.path, LOCALIZATION_FOLDER_NAME, LOCALIZATION_NAME_FILE), 'w')
        f.write("l_english:\n")
        for province in self.idsToProvinces:
            if province != None:
                f.write(" PROV{}:0 \"{}\"\n".format(province.id, province.localizationName))

        print("Saving Adjective Localizations...")
        sys.stdout.flush()
        f = open("{}/{}/{}".format(self.path, LOCALIZATION_FOLDER_NAME, LOCALIZATION_ADJECTIVE_FILE), 'w')
        f.write("l_english:\n")
        for province in self.idsToProvinces:
            if province != None:
                f.write(" ADJ{}:0 \"{}\"\n".format(province.id, province.localizationAdjective))
        
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

        print("Saving Terrain File...")
        sys.stdout.flush()
        writeToFileFromRootNode("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, TERRAIN_FILE_NAME), self.terrainTree)

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

        print("Saving Trade Node Data...")
        sys.stdout.flush()
        writeToFileFromRootNode("{}/{}/{}/{}".format(self.path, COMMON_FOLDER, TRADE_NODE_FOLDER, TRADE_NODES_FILE), self.tradeNodeTree)

        print("Saving Success")
        sys.stdout.flush()
    
    def provinceIsWater(self, province):
        terrainName = province.terrain
        if terrainName in self.terrainTree["categories"]:
            if "is_water" in self.terrainTree["categories"][terrainName]:
                return self.terrainTree["categories"][terrainName]["is_water"].values == "yes"
        return False

def writeFieldIfExists(file, text, field):
    if field != "":
        file.write("{} = {}\n".format(text, field))