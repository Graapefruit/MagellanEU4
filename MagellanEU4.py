import sys
from MagellanClasses.Defaults import DEFAULT_CONTINENTS
from MagellanClasses.MapInfoManager import MapInfoManager
from MagellanClasses.DisplayManager import DisplayManager
from MagellanClasses.Constants import *
from PIL import Image
from os.path import exists
from os import listdir
from random import randint

from MagellanClasses.EU4DataFileParser import *

from Utils.MapMode import MapMode

FAREWELLS = ["drink water", "clean your room", "sleep on time", "stretch", "embargo your rivals", "improve with outraged countries", "do your laundry"]
MAP_MODE_NAMES = {"province", "religion", "culture", "tax", "production", "manpower", "development", "tradeGood", "area", "continet", "hre", "owner", "controller", "terrain", "climate", "weather", "tradeNode", "impassable"}

class MagellanEU4():
	def __init__(self):
		self.currentMapMode = None
		self.currentProvince = None
		self.selectedProvinces = set()
		self.view = DisplayManager()
		self.view.onMenuFileOpen = self.onNewModOpen
		self.view.onMenuFileSave = self.onSave
		self.view.mapDisplay.onLeftClick = self.selectProvince
		self.view.mapDisplay.onRightClick = self.colourProvince
		self.view.onNewMapMode = self.changeMapMode
		self.view.onFieldUpdate = self.updateCurrentProvince
		self.mapModes = dict()
		self.model = None
                
	def selectProvince(self, x, y):
		self.currentProvince = self.model.getProvinceAtIndex(x, y)
		self.view.updateProvinceInfo(self.currentProvince)
		self.selectedProvinces.add(self.currentProvince)

	def colourProvince(self, x, y):
		if self.currentProvince:
			fieldName = self.currentMapMode.name
			if fieldName != "province":
				province = self.model.getProvinceAtIndex(x, y)
				fieldValue = self.currentProvince.getFieldFromString(fieldName)
				self.updateProvince(province, fieldName, fieldValue)

	def updateCurrentProvince(self, fieldName, fieldValue):
		self.updateProvince(self.currentProvince, fieldName, fieldValue)

	# TODO: Discovery
	def updateProvince(self, province, fieldName, fieldValue):
		if province:
			if province.getFieldFromString(fieldName) != fieldValue:
				province.setFieldFromString(fieldName, fieldValue)
				if fieldName in self.mapModes:
					mapMode = self.mapModes[fieldName]
					mapMode.updateProvince(province)
					if self.currentMapMode == mapMode:
						self.view.updateMapMode(self.currentMapMode)

	def onNewModOpen(self, path):
		self.model = MapInfoManager(path)
		self.mapModes = dict()
		colorMappings = {"religion": self.model.religionsToColours, "discovery": {True: (255, 255, 255), False: (96, 96, 96)}}
		for mapModeName in MAP_MODE_NAMES:
			colorMapping = None if mapModeName not in colorMappings else colorMappings[mapModeName]
			self.mapModes[mapModeName] = MapMode(mapModeName, self.model, colorMapping)
		for mapModeName in self.model.techGroups:
			self.mapModes[mapModeName] = MapMode(mapModeName, self.model, colorMappings["discovery"])
		self.mapModes["province"].image = Image.open("{}/{}/{}".format(path, MAP_FOLDER_NAME, PROVINCE_FILE_NAME))
		self.changeMapMode("province")
		self.view.createNewDiscoveryCheckboxes(self.model.techGroups)
		# Combobox Updates
		self.view.terrainField["values"] = list(self.model.terrainTree["categories"].values.keys())
		self.view.tradeNodeField["values"] = list(self.model.tradeNodeTree.values.keys())
		self.view.continentField["values"] = self.getNewComboBoxEntriesFromFile("{}/{}/{}".format(path, MAP_FOLDER_NAME, CONTINENTS_FILE_NAME), CONTINENT_FILE_GROUPING_PATTERN, DEFAULT_CONTINENTS)
		self.view.religionField["values"] = list(self.model.religionsToColours.keys())
		#self.view.cultureField["values"] = self.getNewComboBoxEntriesFromFolder("{}/{}/{}".format(path, COMMON_FOLDER, CULTURES_FOLDER), CULTURES_FILE, CULTURES_GROUPING_PATTERN, DEFAULT_CULTURES)
		#self.view.tradeGoodField["values"] = self.getNewComboBoxEntriesFromFolder("{}/{}/{}".format(path, COMMON_FOLDER, TRADE_GOODS_FOLDER), TRADE_GOODS_FILE, TRADE_GOODS_GROUPING_PATTERN, DEFAULT_TRADE_GOODS)
		print("Map Successfully Loaded")

	def onSave(self):
		self.model.save(self.selectedProvinces)
		self.selectedProvinces = set()

	def changeMapMode(self, mapModeString):
		self.currentMapMode = self.mapModes[mapModeString]
		if self.currentMapMode.image == None:
			print("Generating the {} MapMode for the first time. This will take time...".format(mapModeString))
			self.currentMapMode.generateImage()
		self.view.updateMapMode(self.currentMapMode)

	def getNewComboBoxEntriesFromFile(self, filePath, regexPattern, default):
		newEntries = []
		if exists(filePath):
			matches = re.findall(regexPattern, open(filePath, 'r').read())
			for match in matches:
				newEntries.append(match[0])
		else:
			newEntries = default[:]
		return newEntries

	def getNewComboBoxEntriesFromFolder(self, folderPath, baseFileName, regexPattern, default):
		newEntries = default[:]
		if exists(folderPath):
			if exists(baseFileName):
				newEntries = []
			for fileName in listdir(folderPath):
				matches = re.findall(regexPattern, open("{}/{}".format(folderPath, fileName), 'r', encoding="utf-8").read())
				for match in matches:
					newEntries.append(match)
		return newEntries

if __name__ == "__main__":
	controller = MagellanEU4()
	controller.view.startMainLoop()
	print("Don't forget to {}!".format(FAREWELLS[randint(0, len(FAREWELLS)-1)]))