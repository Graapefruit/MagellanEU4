import imp
import sys
import csv
from Utils.Province import Province
from Utils.RGB import RGB
from MagellanClasses.Constants import *
from PIL import Image

class MapInfoManager():
    def __init__(self, fileFormat):
        self.max_provinces = 5000 # TODO: Grab this from Default.map
        self.populateProvinces(fileFormat.format(MAP_FOLDER_NAME, PROVINCE_DEFINITION_FILE_NAME), self.max_provinces)
        self.provinceMapLocation = fileFormat.format(MAP_FOLDER_NAME, PROVINCE_FILE_NAME)
        self.provinceMapImage = Image.open(fileFormat.format(MAP_FOLDER_NAME, PROVINCE_FILE_NAME)).load()

    def populateProvinces(self, path, maxProvinces):
        print("Parsing " + path + "... ")
        sys.stdout.flush()
        self.provinces = []
        self.colorsToProvinces = dict()
        self.idsToProvinces = [-1] * maxProvinces
        provincesInfo = open(path)
        reader = csv.reader(provincesInfo, delimiter=';')
        for provinceInfo in reader:
            if (provinceInfo[0] == "province"):
                continue
            rgb = RGB(int(provinceInfo[1]), int(provinceInfo[2]), int(provinceInfo[3]))
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

    def getProvinceMapLocation(self):
        return self.provinceMapLocation

    def getProvinceAtIndex(self, x, y):
        return self.colorsToProvinces[RGB.newFromTuple(self.provinceMapImage[x, y])]