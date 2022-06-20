from .MapMode import MapMode

class ProvinceMapMode(MapMode):
    def __init__(self):
        super(ProvinceMapMode, self).__init__()

    def getName(self):
        return "Province"

    def getOrLoadImage(self):
        if not self.image:
            self.image = self.model.provinceMapImage
        return self.image