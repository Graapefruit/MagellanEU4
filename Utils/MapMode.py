from PIL import Image
from random import randint

EMPTY_COLOUR = (255, 255, 255)

class MapMode():
    def __init__(self, name, model, colorMapping):
        self.image = None
        self.name = name
        self.model = model
        self.colorMapping = (colorMapping if colorMapping != None else dict())
        self.colorMapping[""] = EMPTY_COLOUR

    def generateImage(self):
        self.image = Image.new("RGB", self.model.provinceMapImage.size)
        for province in self.model.idsToProvinces:
            if province == None:
                continue
            self.updateProvince(province)

    def updateProvince(self, province):
        if self.image:
            fieldValue = province.getFieldFromString(self.name)
            if not (fieldValue in self.colorMapping):
                self.colorMapping[fieldValue] = (randint(0, 255), randint(0, 255), randint(0, 255))
            for pixel in province.pixels:
                self.image.putpixel(pixel, self.colorMapping[fieldValue])
    
    def _getMaybeAddProvinceColor(self, province):
        fieldValue = province.getFieldFromString(self.name)
        if not (fieldValue in self.colorMapping):
            self.colorMapping[fieldValue] = (randint(0, 255), randint(0, 255), randint(0, 255))
        return self.colorMapping[fieldValue]