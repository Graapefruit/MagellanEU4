import sys
from MagellanClasses.Defaults import DEFAULT_CONTINENTS, DEFAULT_CULTURES, DEFAULT_RELIGIONS, DEFAULT_TECH_GROUPS, DEFAULT_TRADE_GOODS
from MagellanClasses.MapInfoManager import MapInfoManager
from MagellanClasses.DisplayManager import DisplayManager
from MagellanClasses.Constants import *
from PIL import Image
from os.path import exists
from os import listdir
from random import randint

from Utils.MapMode import MapMode

FAREWELLS = ["drink water", "clean your room", "sleep on time", "stretch", "embargo your rivals", "improve with outraged countries", "do your laundry"]

class MagellanEU4():
	def __init__(self):
		self.currentProvince = None
		self.selectedProvinces = set()
		self.view = DisplayManager()
		self.view.onMenuFileOpen = self.onNewModOpen
		self.view.onMenuFileSave = self.onSave
		self.view.mapDisplay.mapClickCallback = self.onPixelClicked
		self.mapModes = dict()
		self.model = None
                
	def onPixelClicked(self, x, y):
		self.updateProvinceInfoModel()
		self.currentProvince = self.model.getProvinceAtIndex(x, y)
		self.view.updateProvinceInfo(self.currentProvince)
		self.selectedProvinces.add(self.currentProvince)

	def updateProvinceInfoModel(self):
		if not self.currentProvince:
			pass # No province selected; ignore
		elif not self.view.taxText.get().isdigit() or not self.view.productionText.get().isdigit() or not self.view.manpowerText.get().isdigit():
			print("ERROR: At least one of tax, production, or manpower is not an integer. Please fix this before selecting another province")
			sys.stdout.flush()
		else:
			self.currentProvince.capital = self.view.capitalField.get()
			self.currentProvince.localizationName = self.view.provinceLocalizationName.get()
			self.currentProvince.localizationAdjective = self.view.provinceLocalizationAdjective.get()
			self.currentProvince.cores = list(map(lambda n: n.strip(), self.view.coresField.get().split(','))) if len(self.view.coresField.get().strip()) > 0 else []
			self.currentProvince.owner = self.view.tagField.get()
			self.currentProvince.controller = self.view.controllerField.get()
			self.currentProvince.culture = self.view.cultureField.get()
			self.currentProvince.religion = self.view.religionField.get()
			self.currentProvince.hre = self.view.hreState.get() == 1
			self.currentProvince.impassable = self.view.impassableState.get() == 1
			self.currentProvince.tax = int(self.view.taxText.get())
			self.currentProvince.production = int(self.view.productionText.get())
			self.currentProvince.manpower = int(self.view.manpowerText.get())
			self.currentProvince.tradeGood = self.view.tradeGoodField.get()
			self.currentProvince.area = self.view.areaField.get()
			self.currentProvince.continent = self.view.continentField.get()
			self.currentProvince.terrain = self.view.terrainField.get()
			self.currentProvince.climate = self.view.climateField.get()
			self.currentProvince.weather = self.view.weatherField.get()
			self.currentProvince.tradeNode = self.view.tradeNodeField.get()
			self.currentProvince.discovered = []
			for techGroup in self.view.techGroupToIntVar:
				if self.view.techGroupToIntVar[techGroup].get() == 1:
					self.currentProvince.discovered.append(techGroup)

	def onNewModOpen(self, path):
		self.model = MapInfoManager(path)
		self.mapModes = dict()
		self.mapModes["province"] = MapMode("province", self.model, None)
		self.mapModes["province"].image = Image.open("{}/{}/{}".format(path, MAP_FOLDER_NAME, PROVINCE_FILE_NAME))
		self.view.updateMapMode(self.mapModes["province"])
		# Combobox Updates
		self.view.terrainField["values"] = list(self.model.terrainTree["categories"].values.keys())
		self.view.tradeNodeField["values"] = list(self.model.tradeNodeTree.values.keys())
		self.view.continentField["values"] = self.getNewComboBoxEntriesFromFile("{}/{}/{}".format(path, MAP_FOLDER_NAME, CONTINENTS_FILE_NAME), CONTINENT_FILE_GROUPING_PATTERN, DEFAULT_CONTINENTS)
		self.view.createNewDiscoveryCheckboxes(self.getNewTechGroupsFromFile("{}/{}/{}".format(path, COMMON_FOLDER, TECHNOLOGY_FILE)))
		self.view.religionField["values"] = self.getNewComboBoxEntriesFromFolder("{}/{}/{}".format(path, COMMON_FOLDER, RELIGIONS_FOLDER), RELIGIONS_FILE, RELIGIONS_GROUPING_PATTERN, DEFAULT_RELIGIONS)
		self.view.cultureField["values"] = self.getNewComboBoxEntriesFromFolder("{}/{}/{}".format(path, COMMON_FOLDER, CULTURES_FOLDER), CULTURES_FILE, CULTURES_GROUPING_PATTERN, DEFAULT_CULTURES)
		self.view.tradeGoodField["values"] = self.getNewComboBoxEntriesFromFolder("{}/{}/{}".format(path, COMMON_FOLDER, TRADE_GOODS_FOLDER), TRADE_GOODS_FILE, TRADE_GOODS_GROUPING_PATTERN, DEFAULT_TRADE_GOODS)

	def onSave(self):
		self.updateProvinceInfoModel()
		self.model.save(self.selectedProvinces)
		self.selectedProvinces = set()

	def getNewComboBoxEntriesFromFile(self, filePath, regexPattern, default):
		newEntries = []
		if exists(filePath):
			matches = re.findall(regexPattern, open(filePath, 'r').read())
			for match in matches:
				newEntries.append(match[0])
		else:
			newEntries = default[:]
		return newEntries

	def getNewTechGroupsFromFile(self, filePath):
		techGroups = []
		if exists(filePath):
			matches = re.findall(TECH_GROUP_GROUPING_PATTERN, open(filePath, 'r').read())
			for match in matches:
				techGroups.append(match)
		else:
			techGroups = DEFAULT_TECH_GROUPS[:]
		return techGroups

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