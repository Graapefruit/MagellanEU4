import sys
import csv
from ProvinceGenerator import PROVINCE_HISTORY_PATH
from Utils.Province import Province
from MagellanClasses.Constants import *
from PIL import Image
import numpy

# TODO:
# 1. History File
# 2. Localization
# 3. Areas, Regions, Subcontinents, Continents
# 4. Tags
class MapInfoManager():
    def __init__(self, fileFormat):
        max_provinces = 5000 # TODO: Grab this from Default.map
        self.provinces = []
        self.colorsToProvinces = dict()
        self.idsToProvinces = [None] * max_provinces
        self.populateFromDefinitionFile(fileFormat.format(MAP_FOLDER_NAME, PROVINCE_DEFINITION_FILE_NAME))
        # self.loadFromHistory(fileFormat.format(MAP_FOLDER_NAME, PROVINCES_HISTORY_PATH))
        self.provinceMapImage = Image.open(fileFormat.format(MAP_FOLDER_NAME, PROVINCE_FILE_NAME))
        self.provinceMapArray = numpy.array(self.provinceMapImage)
        # self.populatePixels()
        self.provinceMapLocation = fileFormat.format(MAP_FOLDER_NAME, PROVINCE_FILE_NAME)

    # --- Setup --- #

    def populateFromDefinitionFile(self, path):
        print("Parsing " + path + "... ")
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

    #def loadFromHistory(self, path):
    #    for province in path:
            
        

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
        return self.colorsToProvinces.get((self.provinceMapArray[y][x][0], self.provinceMapArray[y][x][1], self.provinceMapArray[y][x][2]))

    #def generateReligionMap(self):
