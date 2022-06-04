from .MapMode import MapMode
import sys

class InputController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.mapMode = None

    def changeMapMode(self, newMapMode):
        self.mapMode = newMapMode
        self.view.updateMap(self.mapMode.getOrLoadImage())
                
    def onPixelClicked(self, x, y):
        province = self.model.getProvinceAtIndex(x, y)
        self.view.updateProvinceInfo(province)