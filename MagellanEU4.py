import sys
from MagellanClasses.MapInfoManager import MapInfoManager
from MagellanClasses.DisplayManager import DisplayManager
from MagellanClasses.Constants import *
from PIL import Image
from random import randint

FAREWELLS = ["drink water", "clean your room", "sleep on time", "stretch", "embargo your rivals", "improve with outraged countries"]

class MagellanEU4():
	def __init__(self):
		self.currentProvince = None
		self.selectedProvinces = set()
		self.view = DisplayManager()
		self.view.onMenuFileOpen = self.onNewModOpen
		self.view.onMenuFileSave = self.onSave
		self.view.mapDisplay.mapClickCallback = self.onPixelClicked
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
			sys.stdout.flush()
			self.currentProvince.capital = self.view.provinceCapitalLabel.get()
			self.currentProvince.name = self.view.provinceName.get()
			self.currentProvince.adjective = self.view.provinceAdjective.get()
			self.currentProvince.cores = list(map(lambda n: n.strip(), self.view.coresField.get().split(','))) if not self.view.coresField.get().isspace() else []
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
			self.currentProvince.discovered = []
			for techGroup in self.view.techGroupToIntVar:
				if self.view.techGroupToIntVar[techGroup].get() == 1:
					self.currentProvince.discovered.append(techGroup)


	def onNewModOpen(self, path):
		fileFormat = path + "/{}/{}"
		self.model = MapInfoManager(path)
		self.view.updateMap(Image.open(fileFormat.format(MAP_FOLDER_NAME, PROVINCE_FILE_NAME)))

	def onSave(self):
		self.updateProvinceInfoModel()
		self.model.save(self.selectedProvinces)
		self.selectedProvinces = set()

if __name__ == "__main__":
	controller = MagellanEU4()
	controller.view.startMainLoop()
	print("Don't forget to {}!".format(FAREWELLS[randint(0, len(FAREWELLS)-1)]))