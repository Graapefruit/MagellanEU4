from MagellanClasses.Defaults import DEFAULT_CONTINENTS
from MagellanClasses.MapInfoManager import MapInfoManager
from MagellanClasses.DisplayManager import DisplayManager
from MagellanClasses.Constants import *
from PIL import Image
from os.path import exists
from os import listdir
from random import randint
import sys

from FileParser.EU4DataFileParser import *

from Utils.MapMode import MapMode

FAREWELLS = ["drink water", "clean your room", "sleep on time", "stretch", "embargo your rivals", "improve with outraged countries", "do your laundry", "insult your rivals", "turn off your edicts", "floss your teeth"]
DEVELOPMENT_EXPECTED_RANGE = 39

class MagellanEU4():
	def __init__(self):
		self.currentMapMode = None
		self.currentProvince = None
		self.modifiedProvinces = set()
		self.view = DisplayManager()
		self.view.onMenuFileOpen = self.onNewModOpen
		self.view.onMenuFileSave = self.onSave
		self.view.mapDisplay.onLeftClick = self.selectProvince
		self.view.mapDisplay.onRightClick = self.colourProvince
		self.view.onNewMapMode = self.changeMapMode
		self.view.onFieldUpdate.callback = self.updateCurrentProvince
		self.view.onGeneratePositions = (lambda : self.model.generatePositions())
		self.view.onPropagateOwnerData = (lambda : (self.modifiedProvinces.update(self.model.propagateOwnerData())))
		self.mapModes = dict()
		self.model = None
                
	def selectProvince(self, x, y):
		self.currentProvince = self.model.getProvinceAtIndex(x, y)
		self.view.updateProvinceInfo(self.currentProvince)
		self.modifiedProvinces.add(self.currentProvince)
		if self.currentProvince.owner.lower() in self.model.tagNameDict:
			self.view.tagInfoPanel.setTag(self.model.tagNameDict[self.currentProvince.owner.lower()], self.model.path)
		else:
			self.view.tagInfoPanel.removeTag()

	def colourProvince(self, x, y):
		if self.currentProvince:
			fieldName = self.currentMapMode.name
			if fieldName != "province":
				province = self.model.getProvinceAtIndex(x, y)
				fieldValue = self.currentProvince.getFieldFromString(fieldName)
				self.updateProvince(province, fieldName, fieldValue)

	def updateCurrentProvince(self, fieldName, newFieldValue, sanityCheck):
		if sanityCheck(newFieldValue):
			self.updateProvince(self.currentProvince, fieldName, newFieldValue)
		else:
			print("Error: field {} has malformed input {}! Ignoring...".format(fieldName, newFieldValue))
			sys.stdout.flush()

	def updateProvince(self, province, fieldName, newFieldValue):
		if province:
			if  province.getFieldFromString(fieldName) != newFieldValue:
				province.setFieldFromString(fieldName, newFieldValue)
				if fieldName in self.mapModes:
					mapMode = self.mapModes[fieldName]
					if mapMode.image:
						mapMode.updateProvince(province)
						mapMode.generateImage()
					if self.currentMapMode == mapMode:
						self.view.updateMapMode(self.currentMapMode)
					self.modifiedProvinces.add(province)

	def onNewModOpen(self, path):
		if not exists(path):
			print("ERROR: \"{}\" is not a valid directory!".format(path))
			return
		self.model = MapInfoManager(path)
		self.view.window.title(path)
		self.mapModes = dict()
		colorMappings = {"religion": self.model.religionsToColours, 
			"discovery": {True: (255, 255, 255), False: (96, 96, 96)}, 
			"tradeNode": self.populateTradeNodeMappings(),
			"tax": self.getDevelopmentMappings(DEVELOPMENT_EXPECTED_RANGE // 3),
			"production": self.getDevelopmentMappings(DEVELOPMENT_EXPECTED_RANGE // 3),
			"manpower": self.getDevelopmentMappings(DEVELOPMENT_EXPECTED_RANGE // 3),
			"development": self.getDevelopmentMappings(DEVELOPMENT_EXPECTED_RANGE),
			"hre": {True: (0, 255, 0), False: (255, 0, 0)},
			"climate": {"": (102, 127, 68), "temperate": (102, 127, 68), "arctic": (255, 255, 255), "tropical": (102, 178, 48), "arid": (216, 214, 66)},
			"weather": {"": (0, 0, 0), "no_winter": (0, 0, 0), "mild_winter": (85, 85, 85), "normal_winter": (170, 170, 170), "severe_winter": (255, 255, 255), "mild_monsoon": (0, 0, 85), "normal_monsoon": (0, 0, 170), "severe_monsoon": (0, 0, 255)},
			"impassable": {True: (0, 0, 0), False: (96, 96, 96)},
			"terrain": self.model.terrainsToColours,
			"isSea": {True: (0, 255, 255), False: (64, 64, 64)},
			"isLake": {True: (0, 255, 255), False: (64, 64, 64)},
			"tradeGood": self.model.tradeGoodsToColours,
			"owner": self.model.tagsToColours,
			"controller": self.model.tagsToColours}

		for mapModeName in MAP_MODE_DISPLAY_TO_NAME.values():
			colorMapping = None if mapModeName not in colorMappings else colorMappings[mapModeName]
			self.mapModes[mapModeName] = MapMode(mapModeName, self.model, colorMapping)
		for mapModeName in self.model.techGroups:
			self.mapModes[mapModeName] = MapMode(mapModeName, self.model, colorMappings["discovery"])
		self.mapModes["province"].image = Image.open("{}/{}/{}".format(path, MAP_FOLDER_NAME, PROVINCE_FILE_NAME))
		self.changeMapMode("province")
		self.view.createNewDiscoveryCheckboxes(self.model.techGroups)
		# Combobox Updates
		self.view.terrainField["values"] = list(self.model.terrainTree["categories"].value.keys())
		self.view.tradeNodeField["values"] = list(self.model.tradeNodeTree.value.keys())
		self.view.continentField["values"] = self.getNewComboBoxEntriesFromFile("{}/{}/{}".format(path, MAP_FOLDER_NAME, CONTINENTS_FILE_NAME), CONTINENT_FILE_GROUPING_PATTERN, DEFAULT_CONTINENTS)
		self.view.religionField["values"] = list(self.model.religionsToColours.keys())
		self.view.tradeGoodField["values"] = list(self.model.tradeGoodsToColours.keys())
		self.view.ownerField["values"] = list(self.model.tagsToColours.keys())
		self.view.controllerField["values"] = list(self.model.tagsToColours.keys())
		print("Mod Successfully Loaded")

	def getDevelopmentMappings(self, max):
		devToColours = dict()
		yellowMin = max//2
		for i in range(1, yellowMin+1):
			devToColours[i] = (255, (255 // yellowMin) * i, 0)
		for i in range(yellowMin+1, max+1):
			devToColours[i] = ((255 // yellowMin) * (yellowMin - i), 255, 0)
		return devToColours

	def populateTradeNodeMappings(self):
		tradeNodeMappings = dict()
		for tradeNode in self.model.tradeNodeTree.getChildren():
			if "color" in tradeNode.value:
				rgb = tuple(map((lambda n : int(n)), tradeNode["color"]))
				tradeNodeMappings[tradeNode.name] = rgb
		return tradeNodeMappings

	def onSave(self):
		self.model.save(self.modifiedProvinces)
		self.modifiedProvinces = set()

	def changeMapMode(self, mapModeString):
		self.currentMapMode = self.mapModes[mapModeString]
		if self.currentMapMode.image == None:
			print("Generating the {} MapMode for the first time. This will take time...".format(mapModeString))
			self.currentMapMode.initializeMapMode()
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