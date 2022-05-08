import os.path
from PIL import Image, ImageTk
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
RNW_PROVINCE_KEY = "RNW"
GROUPING_PATTERN = re.compile("([a-z_]+)\s*=\s*{([a-z0-9_\s]*)}", re.IGNORECASE)
AREA_GROUPING_PATTERN = re.compile("([a-z_]+)\s*=\s*{\s*(color\s*=\s*{\s*[0-9]{1,3}\s*[0-9]{1,3}\s*[0-9]{1,3}\s*})?([a-z0-9_\s]*)}", re.IGNORECASE)
AREA_COLOR_GROUPING_PATTERN = re.compile("([0-9]{1,3})\s*([0-9]{1,3})\s*([0-9]{1,3})")
REGION_GROUPING_PATTERN = re.compile("([a-z_]+)\s*=\s*{\s*areas\s*=\s*{([a-z0-9_\s]*)}[monsoon0-9.={}\s]*}", re.IGNORECASE) # Note that monsoons are ignored. They will have to be done manually, or add this feature in later

class Terrain(Enum):
	AUTO = 1

class Climate(Enum):
	TEMPERATE = 1
	ARID = 2
	TROPICAL = 3
	ARCTIC = 4

class RGB:
	def __init__(self, red, green, blue):
		self.red = red
		self.green = green
		self.blue = blue

	def __eq__(self, other):
		return self.red == other.red and self.green == other.green and self.blue == other.blue 

	def __str__(self):
		return "Red: {}, Green: {}, Blue: {}".format(self.red, self.green, self.blue)

	# Hash is the html representation of the number as a decimal
	def __hash__(self):
		return int(self.getHtmlColor(), base=16)

	def getHtmlColor(self):
		return self.__getColorHexString__(self.red) + self.__getColorHexString__(self.green) + self.__getColorHexString__(self.blue)

	def __getColorHexString__(self, color):
		h = hex(color)[2:]
		if len(h) == 1:
			return "0" + h
		return h

#class Pixel:
#	def __init__(self, x, y):
#		self.x = x
#		self.y = y

class Province:
	def __init__(self, id, color, key):
		self.color = color
		# self.pixels = []
		self.id = id
		self.key = key
		self.parentGrouping = None
		self.continent = None
		# self.climate = None
		# self.terrain = None

	def __str__(self):
		return "Province {0} with id {1} of colour {2} in area {3} in continent {4} with {5} pixels".format(self.name, self.id, self.color, self.area, self.continent, len(self.pixels))

class Grouping:
	def __init__(self, name):
		self.name = name
		self.subGroupings = []
		self.parentGrouping = None

	def __str__(self):
		return "Grouping {0}: {1}. Belongs to {2}".format(self.name, self.subGroupings, self.parentGrouping)

	@staticmethod
	def populate(path, subGroupings):
		print("Parsing " + path + "... ")
		f = getFileStringWithoutComments(open(path, "r"))
		groupings = []
		keysToGroupings = dict()
		matches = GROUPING_PATTERN.findall(f)
		for match in matches:
			grouping = Grouping(match[0])
			for subGrouping in match[1].split():
				grouping.subGroupings.append(subGrouping)
				subGroupings[subGrouping].parentGrouping = grouping
			groupings.append(grouping)
			keysToGroupings[match[0]] = grouping
		return groupings, keysToGroupings

class Area(Grouping):
	def __init__(self, name):
		super().__init__(name)
		self.color = None

	@staticmethod
	def populate(path, subGroupings):
		print("Parsing " + path + "... ")
		f = getFileStringWithoutComments(open(path, "r"))
		areas = []
		keysToAreas = dict()
		matches = AREA_GROUPING_PATTERN.findall(f)
		for match in matches:
			area = Area(match[0])
			if match[1] != "":
				r, g, b = AREA_COLOR_GROUPING_PATTERN.findall(match[1])[0]
				area.color = RGB(int(r), int(g), int(b))
			area.subGroupings = match[2].split()
			for subGrouping in match[2].split():
				area.subGroupings.append(subGrouping)
				subGroupings[subGrouping].area = area
			areas.append(area)
			keysToAreas[match[0]] = area
		return areas, keysToAreas

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

#def populateProvinceInfo(path, colorToProvinces):
#	print("Parsing " + path + "... ")
#	provinces = []
#	provincesInfo = open(path)
#	reader = csv.reader(provincesInfo, delimiter=';')
#	for provinceInfo in reader:
#		# The first line is a header; ignore it
#		if (provinceInfo[0] == "province"):
#			continue
#		rgb = RGB(int(provinceInfo[1]), int(provinceInfo[2]), int(provinceInfo[3]))
#		if (rgb in colorToProvinces):
#			province = colorToProvinces[rgb]
#			province.id = int(provinceInfo[0])
#			province.name = provinceInfo[4]
#			provinces.append(province)
#	return provinces

def populateProvinces(path):
	print("Parsing " + path + "... ")
	provinces = []
	colorsToProvinces = dict()
	idsToProvinces = dict()
	provincesInfo = open(path)
	reader = csv.reader(provincesInfo, delimiter=';')
	for provinceInfo in reader:
		if (provinceInfo[0] == "province"):
			continue
		rgb = RGB(int(provinceInfo[1]), int(provinceInfo[2]), int(provinceInfo[3]))
		# Skip RNW Provinces: some even share the same colors
		if (provinceInfo[4] == RNW_PROVINCE_KEY):
			continue
		if (rgb in colorsToProvinces):
			print("ERROR: Two provinces share the same colour! IDs: {} {}".format(colorsToProvinces[rgb].id, provinceInfo[0]))
			quit()
		province = Province(int(provinceInfo[0]), rgb, provinceInfo[4])
		provinces.append(province)
		colorsToProvinces[rgb] = province
		idsToProvinces[provinceInfo[0]] = province
	return provinces, colorsToProvinces, idsToProvinces

def populateGrouping(path, regexPattern):
	print("Parsing " + path + "... ")
	f = getFileStringWithoutComments(open(path, "r"))
	groupings = []
	matches = regexPattern.findall(f)
	for match in matches:
		grouping = Grouping(match[0])
		grouping.subGroupings = match[1].split()
		groupings.append(grouping)
	return groupings

def populateArea(path, idsToProvinces):
	print("Parsing " + path + "... ")
	f = getFileStringWithoutComments(open(path, "r"))
	areas = []
	matches = AREA_GROUPING_PATTERN.findall(f)
	for match in matches:
		area = Area(match[0])
		if match[1] != "":
			r, g, b = AREA_COLOR_GROUPING_PATTERN.findall(match[1])[0]
			area.color = RGB(int(r), int(g), int(b))
		area.subGroupings = match[2].split()
		for subGrouping in match[2].split():
			area.subGroupings.append(subGrouping)
			idsToProvinces[subGrouping].area = area
		areas.append(area)
	return areas

def getFileStringWithoutComments(f):
	s = ""
	for line in f.readlines():
		i = line.find('#')
		if i != -1:
			s += line[:i]
		else:
			s += line
	return s



if __name__ == "__main__":
	directoryName = input("Please enter the full path to your mod folder: ")
	fileFormat = directoryName + "/{}/{}"
	provinces, colorsToProvinces, idsToProvinces = populateProvinces(fileFormat.format(MAP_FOLDER_NAME, PROVINCE_DEFINITION_FILE_NAME))
	areas, keysToAreas = Area.populate(fileFormat.format(MAP_FOLDER_NAME, AREAS_FILE_NAME), idsToProvinces)
	#regions = Region.populate(fileFormat.format(MAP_FOLDER_NAME, REGIONS_FILE_NAME), idsToProvinces)
	#superRegions = Grouping.populate(fileFormat.format(MAP_FOLDER_NAME, SUPERREGIONS_FILE_NAME))
	#continents = populateGrouping(fileFormat.format(MAP_FOLDER_NAME, CONTINENTS_FILE_NAME), GROUPING_PATTERN)

	# window = tkinter.Tk()
	# mapImage = Image.open(fileFormat.format(MAP_FOLDER_NAME, PROVINCE_FILE_NAME))
	# test = ImageTk.PhotoImage(mapImage)

	# label1 = tkinter.Label(image=test)
	# label1.image = test
	# label1.place(x=10, y=10)
	# window.mainloop()

