from MagellanClasses.MapInfoManager import MapInfoManager
from MagellanClasses.DisplayManager import DisplayManager
from MagellanClasses.Constants import *
from PIL import Image

class MagellanEU4():
	def __init__(self):
		self.currentProvince = None
		self.view = DisplayManager()
		self.view.onMenuFileOpen = self.onNewModOpen
		self.view.mapDisplay.mapClickCallback = self.onPixelClicked
		self.model = None
                
	def onPixelClicked(self, x, y):
		self.currentProvince = self.model.getProvinceAtIndex(x, y)
		self.view.updateProvinceInfo(self.currentProvince)

	def onNewModOpen(self, path):
		fileFormat = path + "/{}/{}"
		self.model = MapInfoManager(path)
		self.view.updateMap(Image.open(fileFormat.format(MAP_FOLDER_NAME, PROVINCE_FILE_NAME)))

if __name__ == "__main__":
	controller = MagellanEU4()
	controller.view.startMainLoop()
