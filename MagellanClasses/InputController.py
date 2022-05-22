from .MapMode import MapMode

class InputController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.mapMode = None

    def changeMapMode(self, newMapMode):
        self.mapMode = newMapMode
        match self.mapMode:
            case MapMode.PROVINCES:
                self.view.updateMapFromFile(self.model.getProvinceMapLocation())

    def onPixelClicked(self, x, y):
        print("{} {}".format(x, y))