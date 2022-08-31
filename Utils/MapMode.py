from PIL import Image
from random import randint
from .RGB import RGB

class MapMode():
    def __init__(self, name, model, colorMapping):
        self.image = None
        self.name = name
        self.model = model
        self.colorMapping = (colorMapping if colorMapping != None else dict())

    def generateImage(self):
        self.image = Image.new("RGB", self.model.provinceMapImage.size)
        for province in self.model.idsToProvinces:
            color = self._getMaybeAddProvinceColor(province)
            for pixel in province.pixels:
                self.image.putpixel((pixel.x, pixel.y), color)
    
    def _getMaybeAddProvinceColor(self, province):
        fieldValue = ""
        match self.name:
            case "religion":
                fieldValue = province.religion
            case _:
                print("ERROR: Map type \"{}\" cannot be populated".format(self.name))

        if not (fieldValue in self.colorMapping):
            self.colorMapping[fieldValue] = RGB(randint(0, 255), randint(0, 255), randint(0, 255))
        return self.colorMapping[fieldValue]