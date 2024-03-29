from PIL import Image
from random import randint
import numpy as np
from sys import stdout

EMPTY_COLOUR = (255, 255, 255)
PROVINCE_COLOUR_ALPHA = 0.2 # 0 = no influence; 1 = all influence

class MapMode():
    def __init__(self, name, model, colorMapping):
        self.image = None
        self.pixels = np.zeros(model.provinceMapArray.shape).astype('uint8')
        self.name = name
        self.model = model
        self.colorMapping = (colorMapping if colorMapping != None else dict())
        if not "" in self.colorMapping:
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
            color = self.getProvinceColour(province)
            self.pixels[province.pixels[:,1], province.pixels[:,0]] = color

    def getProvinceColour(self, province):
        fieldValue = province.getFieldFromString(self.name)
        if isinstance(fieldValue, str):
            fieldValue = fieldValue.lower()
        if not (fieldValue in self.colorMapping):
            newColour = np.array([randint(0, 255), randint(0, 255), randint(0, 255)])
            print("New field value for mapmode \"{}\": \"{}\". It's colour shall be {}".format(self.name, fieldValue, newColour))
            stdout.flush()
            self.colorMapping[fieldValue] = newColour
        fieldColor = self.colorMapping[fieldValue]
        red = province.color[0] * PROVINCE_COLOUR_ALPHA + fieldColor[0] * (1 - PROVINCE_COLOUR_ALPHA)
        green = province.color[1] * PROVINCE_COLOUR_ALPHA + fieldColor[1] * (1 - PROVINCE_COLOUR_ALPHA)
        blue = province.color[2] * PROVINCE_COLOUR_ALPHA + fieldColor[2] * (1 - PROVINCE_COLOUR_ALPHA)
        return (red, green, blue)