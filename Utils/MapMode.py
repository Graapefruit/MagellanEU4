from PIL import Image
from random import randint
import numpy as np

EMPTY_COLOUR = (255, 255, 255)

class MapMode():
    def __init__(self, name, model, colorMapping):
        self.image = None
        self.pixels = np.zeros(model.provinceMapArray.shape).astype('uint8')
        self.name = name
        self.model = model
        self.colorMapping = (colorMapping if colorMapping != None else dict())
        self.colorMapping[""] = EMPTY_COLOUR

    def initializeMapMode(self):
        self.image = Image.new("RGB", self.model.provinceMapImage.size)
        for province in self.model.idsToProvinces:
            if province == None or len(province.pixels) == 0:
                continue
            self.updateProvince(province)
        self.generateImage()

    def generateImage(self):
        self.image = Image.fromarray(self.pixels, 'RGB')

    def updateProvince(self, province):
        if self.image:
            fieldValue = province.getFieldFromString(self.name)
            if not (fieldValue in self.colorMapping):
                self.colorMapping[fieldValue] = np.array([randint(0, 255), randint(0, 255), randint(0, 255)])
            color = self.colorMapping[fieldValue]
            self.pixels[province.pixels[:,1], province.pixels[:,0]] = color