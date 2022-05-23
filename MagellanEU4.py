import os.path
from enum import Enum
import re
import sys
from MagellanClasses.MapMode import MapMode
from Utils.RGB import RGB
from MagellanClasses.MapInfoManager import MapInfoManager
from MagellanClasses.DisplayManager import DisplayManager
from MagellanClasses.Constants import *
from MagellanClasses.InputController import InputController

class Climate(Enum):
	TEMPERATE = 1
	ARID = 2
	TROPICAL = 3
	ARCTIC = 4

class Winter(Enum):
	NONE = 1
	MILD_WINTER = 2
	NORMAL_WINTER = 3
	SEVERE_WINTER = 4

class Grouping:
	def __init__(self, name):
		self.name = name
		self.subGroupings = []
		self.parentGrouping = None

	def __str__(self):
		return "Grouping {0}: {1}. Belongs to {2}".format(self.name, self.subGroupings, self.parentGrouping)

class Area(Grouping):
	def __init__(self, name):
		super().__init__(self, name)
		self.color = None

class Region(Grouping):
	def __init__(self, name):
		super().__init__(self, name)
		self.monsoonDates = []


# class MonsoonDate:
# 	def __init__(self, start, end):
# 		self.start = start
#		self.end = end

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

def populateArea(path):
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

def populateRegion(path):
	print ("Parsing {}...".format(path))
	f = getFileStringWithoutComments(open(path, "r"))
	regions = []
	keysToRegions = dict()

def populateGrouping(path):
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

def getFileStringWithoutComments(f):
	s = ""
	for line in f.readlines():
		i = line.find('#')
		if i != -1:
			s += line[:i]
		else:
			s += line
	return s

def onMouseMapClick(x, y):
	print("x = {}, y = {}".format(x, y))
	sys.stdout.flush()

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: ({}) (Base Game Folder) (Mod Folder)".format(sys.argv[0]))
		quit()
	baseGamePath = sys.argv[1]
	modPath = sys.argv[2]
	fileFormat = modPath + "/{}/{}"
	# areas, keysToAreas = populateArea(fileFormat.format(MAP_FOLDER_NAME, AREAS_FILE_NAME), idsToProvinces)
	#regions = Region.populate(fileFormat.format(MAP_FOLDER_NAME, REGIONS_FILE_NAME), idsToProvinces)
	#superRegions = Grouping.populate(fileFormat.format(MAP_FOLDER_NAME, SUPERREGIONS_FILE_NAME))
	#continents = populateGrouping(fileFormat.format(MAP_FOLDER_NAME, CONTINENTS_FILE_NAME), GROUPING_PATTERN)
	model = MapInfoManager(fileFormat)# fileFormat.format(MAP_FOLDER_NAME, PROVINCE_FILE_NAME))
	view = DisplayManager(windowName=modPath.split("/")[-1])
	controller = InputController(model=model, view=view)

	view.mapDisplay.mapClickCallback = controller.onPixelClicked
	controller.changeMapMode(MapMode.PROVINCES)
	view.startMainLoop()
