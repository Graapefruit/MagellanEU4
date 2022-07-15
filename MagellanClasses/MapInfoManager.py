import sys
import csv
from Utils.Province import Province
from Utils.Terrain import Terrain
from Utils.RGB import RGB
from MagellanClasses.Constants import *
from PIL import Image
from os import listdir
from os.path import exists
import re
import numpy

# TODO:
# 1. History File
# 2. Localization
# 3. Areas, Regions, Subcontinents, Continents
# 4. Tags
class MapInfoManager():
    def __init__(self, path):
        self.path = path
        self.max_provinces = 5000 # TODO: Grab this from Default.map
        self.provinces = []
        self.areasToColors = dict()
        self.namesToTerrains = dict()
        self.colorsToProvinces = dict()
        self.idsToProvinces = [None] * self.max_provinces
        self.populateFromDefinitionFile("{}/{}/{}".format(path, MAP_FOLDER_NAME, PROVINCE_DEFINITION_FILE_NAME))
        self.populateProvinceHistoryFiles("{}/{}".format(path, PROVINCES_HISTORY_PATH))
        self.populateAreaData("{}/{}/{}".format(path, MAP_FOLDER_NAME, AREAS_FILE_NAME))
        self.populateProvinceTerrain("{}/{}/{}".format(path, MAP_FOLDER_NAME, TERRAIN_FILE_NAME))
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
            if (provinceInfo[0] == "province"):
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
                provinceHistoryFile = open("{}/{}".format(path, fileName), 'r')
                for line in provinceHistoryFile:
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
                            case _:
                                province.extraText += line

    def populateAreaData(self, path):
        print("Populating Areas...")
        sys.stdout.flush()
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

    def populateProvinceTerrain(self, path):
        if exists(path):
            print("Parsing the Terrain.txt")
            sys.stdout.flush()
            terrainFile = open(path, 'r')
            matches = re.findall(TERRAIN_FILE_GROUPING_PATTERN, terrainFile.read())
            for match in matches:
                terrainName = match[0]
                startText = match[1].strip()
                color = RGB.newFromTuple(match[2].split())
                middleText = match[3].strip()
                if len(match[4]) > 0:
                    self.populateProvinceTerrainData(terrainName, match[4])
                endText = match[5].strip()
                newTerrain = Terrain(terrainName, color, startText, middleText, endText)
                self.namesToTerrains[terrainName] = newTerrain
        else:
            print("No Terrain.txt File Found")
            sys.stdout.flush()

    def populateProvinceTerrainData(self, terrainName, text):
        lines = text.split('\n')
        # On the first line, read any potential entries after the curly brace
        lines[0] = lines[0].split('{')[1]
        for line in lines:
            # Remove Comments
            line = line.split('#')[0]
            potentialIds = line.split(' ')
            for potentialId in potentialIds:
                if potentialId.isdigit():
                    provinceId = int(potentialId)
                    if provinceId <= self.max_provinces and self.idsToProvinces[provinceId]:
                        self.idsToProvinces[provinceId].terrain = terrainName
                    else:
                        pass
                        # print("Warning: Terrain {} overrides provinceId {}, which is unused or out of bounds!".format(terrainName, potentialId))
            
    def populatePixels(self):
        #TODO: Slow-ish. Multithread?
        print("Populating Pixels... This may take a while")
        sys.stdout.flush()
        for y in range(0, len(self.provinceMapArray)):
            sys.stdout.flush()
            for x in range(0, len(self.provinceMapArray[y])):
                self.getProvinceAtIndex(x, y).pixels.append((x, y))


    # --- Utility --- #

    # --- Public --- #

    def getProvinceAtIndex(self, x, y):
        province = self.colorsToProvinces.get((self.provinceMapArray[y][x][0], self.provinceMapArray[y][x][1], self.provinceMapArray[y][x][2]))
        return province
    #def generateReligionMap(self):

    def save(self, updatedProvinces):
        areasToProvinces = dict()
        terrainsToProvinces = dict()
        print("Saving History Files...")
        sys.stdout.flush()
        for province in updatedProvinces:
            f = open("{}/{}/{}".format(self.path, PROVINCES_HISTORY_PATH, province.historyFile), 'w')
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
            f.close()

        for province in self.provinces:
            if province.area != "":
                if province.area in areasToProvinces:
                    areasToProvinces[province.area].append(province.id)
                else:
                    areasToProvinces[province.area] = [province.id]
            
            if province.terrain != "":
                if province.terrain in terrainsToProvinces:
                    terrainsToProvinces[province.terrain].append(province.id)
                else:
                    terrainsToProvinces[province.terrain] = [province.id]
        
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
        f = open("{}/{}/{}".format(self.path, MAP_FOLDER_NAME, TERRAIN_FILE_NAME), 'w')
        f.write("categories = {\n")
        f.write("\tpti = {\n\t\ttype = pti\n\t}\n\n") # PTI is not matched by our regex but must still be included
        for terrainName in terrainsToProvinces:
            terrain = None
            if terrainName in self.namesToTerrains:
                terrain = self.namesToTerrains[terrainName]
            else:
                terrain = Terrain(terrainName, RGB(0, 0, 0), "", "", "")
            f.write("\t{} = {{\n".format(terrainName))
            if terrain.startText != "":
                f.write("\t\t{}\n".format(terrain.startText))
            f.write("\t\tcolor = {{ {} {} {} }}\n".format(terrain.color.red, terrain.color.green, terrain.color.blue))
            if terrain.middleText != "":
                f.write("\t\t{}\n".format(terrain.middleText))
            if len(terrainsToProvinces[terrainName]) > 0:
                f.write("\t\tterrain_override = {\n\t\t\t")
                for province in terrainsToProvinces[terrainName]:
                    f.write("{} ".format(province))
                f.write("\n\t\t}")
            f.write("\n\t}\n")
            if terrain.endText != "":
                f.write("\t\t{}\n".format(terrain.endText))
        f.close()

        print("Done.")
        sys.stdout.flush()



def writeFieldIfExists(file, text, field):
    if field != "":
        file.write("{} = {}".format(text, field))