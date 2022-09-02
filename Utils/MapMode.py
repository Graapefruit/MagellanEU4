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
            if province == None:
                continue
            colorRGB = self._getMaybeAddProvinceColor(province)
            color = (colorRGB.red, colorRGB.green, colorRGB.blue)
            for pixel in province.pixels:
                self.image.putpixel((pixel[0], pixel[1]), color)
    
    def _getMaybeAddProvinceColor(self, province):
        fieldValue = ""
        match self.name:
            case "religion":
                fieldValue = province.religion
            case "culture":
                fieldValue = province.culture
            case "tax":
                fieldValue = province.tax
            case "production":
                fieldValue = province.production
            case "manpower":
                fieldValue = province.manpower
            case "development":
                fieldValue = province.tax + province.production + province.manpower
            case "tradeGood":
                fieldValue = province.tradeGood
            case "area":
                fieldValue = province.area
            case "continent":
                fieldValue = province.continent
            case "hre":
                fieldValue = province.hre
            case "owner":
                fieldValue = province.owner
            case "controller":
                fieldValue = province.controller
            #case "cores":
            #    fieldValue = province.cores
            case "terrain":
                fieldValue = province.terran
            case "climate":
                fieldValue = province.climate
            case "weather":
                fieldValue = province.weather
            case "tradeNode":
                fieldValue = province.tradeNode
            case "impassable":
                fieldValue = province.impassable
            case _:
                print("ERROR: Map type \"{}\" cannot be populated".format(self.name))

        if not (fieldValue in self.colorMapping):
            self.colorMapping[fieldValue] = RGB(randint(0, 255), randint(0, 255), randint(0, 255))
        return self.colorMapping[fieldValue]