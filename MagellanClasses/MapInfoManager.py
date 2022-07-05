import sys
import csv
from Utils.Province import Province
from Utils.Terrain import Terrain
from Utils.RGB import RGB
from MagellanClasses.Constants import *
from PIL import Image
from os import listdir
import re
import numpy


# TODO:
# 1. History File
# 2. Localization
# 3. Areas, Regions, Subcontinents, Continents
# 4. Tags
class MapInfoManager():
    def __init__(self, path):
        self.max_provinces = 5000 # TODO: Grab this from Default.map
        self.provinces = []
        self.colorsToProvinces = dict()
        self.namesToTerrains = dict()
        self.idsToProvinces = [None] * self.max_provinces
        self.populateFromDefinitionFile("{}/{}/{}".format(path, MAP_FOLDER_NAME, PROVINCE_DEFINITION_FILE_NAME))
        self.populateProvinceHistoryFiles("{}/{}".format(path, PROVINCES_HISTORY_PATH))
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
                            case "trade_goods":
                                province.tradeGood = lineVal
                            case "discovered_by":
                                province.discovered.append(lineVal)

    def populateProvinceTerrain(self, path):
        print("Parsing the Terrain.txt")
        sys.stdout.flush()
        terrainFile = open(path, 'r')
        matches = re.findall(TERRAIN_FILE_GROUPING_PATTERN, terrainFile.read())
        for match in matches:
            terrainName = match[0]
            startText = match[1]
            color = RGB.newFromTuple(match[2].split())
            middleText = match[3]
            provinceIds = []
            if len(match[4]) > 0:
                provinceIds = self.getProvincesFromTerrainText(terrainName, match[4])
            endText = match[5]
            newTerrain = Terrain(terrainName, color, provinceIds, startText, middleText, endText)
            self.namesToTerrains[terrainName] = newTerrain

    def getProvincesFromTerrainText(self, terrainName, text):
        provinceIds = []
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
                        provinceIds.append(provinceId)
                    else:
                        pass
                        # print("Warning: Terrain {} overrides provinceId {}, which is unused or out of bounds!".format(terrainName, potentialId))
        return provinceIds
            
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
