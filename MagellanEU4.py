import os.path
from PIL import Image
from enum import Enum
import csv
import tkinter
import re

MAP_FOLDER_NAME = "map"
LOCALIZATION_FOLDER_NAME = "localisation"
PROVINCE_FILE_NAME = "provinces.bmp"
PROVINCE_DEFINITION_FILE_NAME = "definition.csv"
DEFAULT_FILE_NAME = "default.map"
ADJACENCIES_FILE_NAME = "adjacencies.csv"
AREAS_FILE_NAME = "area.txt"
REGIONS_FILE_NAME = "region.txt"
SUPERREGIONS_FILE_NAME = "superregion.txt"
CONTINENTS_FILE_NAME = "continent.txt"
POSITIONS_FILE_NAME = "positions.txt"
TERRAIN_FILE_NAME = "terrain.txt"
MAP_FOLDER_NAME = "map"
GROUPING_PATTERN = re.compile("([a-z_]+)\s*=\s*{([#a-z0-9_\s]*)}", re.IGNORECASE)
REGION_GROUPING_PATTERN = re.compile("([a-z_]+)\s*=\s*{\s*areas\s*=\s*{([#a-z0-9_\s]*)}[monsoon0-9.={}\s]*}", re.IGNORECASE) # Note that monsoons are ignored. They will have to be done manually, or add this feature in later

class Terrain(Enum):
	AUTO = 1

class Climate(Enum):
	TEMPERATE = 1
	ARID = 2
	TROPICAL = 3
	ARCTIC = 4

class RGB:
	def __init__(self, red, blue, green):
		self.red = red
		self.green = green
		self.blue = blue

	def __eq__(self, other):
		return self.red == other.red and self.green == other.green and self.blue == other.blue 

	# Hash the HTML code of the color
	def __hash__(self):
		return hash(self.getHtmlColor())

	def getHtmlColor(self):
		return self.__getColorHexString__(self.red) + self.__getColorHexString__(self.green) + self.__getColorHexString__(self.blue)

	def __getColorHexString__(self, color):
		h = hex(color)[2:]
		if len(h) == 1:
			return "0" + h
		return h

class Pixel:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Province:
	def __init__(self, color):
		self.color = color
		self.pixels = []
		self.name = None
		self.id = None
		self.area = None
		self.continent = None
		self.climate = None
		self.terrain = None

	def __str__(self):
		return "Province {0} with id {1} of colour {2} in area {3} in continent {4} with {5} pixels".format(self.name, self.id, self.color, self.area, self.continent, len(self.pixels))

class Grouping:
	def __init__(self, name):
		self.name = name
		self.subGroupings = []
		self.parentGrouping = None

	def __str__(self):
		return "Grouping {0}: {1}. Belongs to {2}".format(self.name, self.subGroupings, self.parentGrouping)

# class MonsoonDate:
# 	def __init__(self, start, end):
# 		self.start = start
#		self.end = end

# class Region(Grouping):
#	def __init__(self, name):
#		super.__init__()
#		self.monsoonDates = []

# class Adjacency:

# def loadProvinces(path):
#	print("Parsing " + path + "... ")
#	provinceMap = Image.open(path)
#	width, height = provinceMap.size
#	colorToProvinces = dict()
#	for y in range(0, height):
#		for x in range(0, width):
#			r, g, b = provinceMap.getpixel((x, y))
#			pixel = Pixel(x, y)
#			color = RGB(r, g, b)
#			if color in colorToProvinces:
#				colorToProvinces[color].pixels.append(pixel)
#			else:
#				colorToProvinces[color] = Province(color)
#	return colorToProvinces

def populateProvinceInfo(path, colorToProvinces):
	print("Parsing " + path + "... ")
	provinces = []
	provincesInfo = open(path)
	reader = csv.reader(provincesInfo, delimiter=';')
	for provinceInfo in reader:
		# The first line is a header; ignore it
		if (provinceInfo[0] == "province"):
			continue
		rgb = RGB(int(provinceInfo[1]), int(provinceInfo[2]), int(provinceInfo[3]))
		if (rgb in colorToProvinces):
			province = colorToProvinces[rgb]
			province.id = int(provinceInfo[0])
			province.name = provinceInfo[4]
			provinces.append(province)
	return provinces

def populateGrouping(path, regexPattern):
	print("Parsing " + path + "... ")
	f = open(path, "r").read()
	groupings = []
	matches = regexPattern.findall(f)
	for match in matches:
		grouping = Grouping(match[0])
		grouping.subGroupings = removeCommentsAndGetSubgroupings(match[1])
		groupings.append(grouping)
	return groupings

def removeCommentsAndGetSubgroupings(grouping):
	subGroupings = []
	for line in grouping.split('\n'):
		poundIndex = line.find("#")
		if poundIndex != -1:
			line = line[0:poundIndex]
		subGroupings += line.split()
	return subGroupings




if __name__ == "__main__":
	directoryName = input("Please enter the full path to your mod folder: ")
	fileFormat = directoryName + "/{}/{}"
	# colorToProvinces = loadProvinces(fileFormat.format(MAP_FOLDER_NAME, PROVINCE_FILE_NAME))
	# provinces = populateProvinceInfo(fileFormat.format(MAP_FOLDER_NAME, PROVINCE_DEFINITION_FILE_NAME), colorToProvinces)
	areas = populateGrouping(fileFormat.format(MAP_FOLDER_NAME, AREAS_FILE_NAME), GROUPING_PATTERN)
	regions = populateGrouping(fileFormat.format(MAP_FOLDER_NAME, REGIONS_FILE_NAME), REGION_GROUPING_PATTERN)
	superRegions = populateGrouping(fileFormat.format(MAP_FOLDER_NAME, SUPERREGIONS_FILE_NAME), GROUPING_PATTERN)
	continents = populateGrouping(fileFormat.format(MAP_FOLDER_NAME, CONTINENTS_FILE_NAME), GROUPING_PATTERN)

