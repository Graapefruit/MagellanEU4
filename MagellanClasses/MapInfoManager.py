import sys

class MapInfoManager():
    def __init__(self, provinceMapLocation):
        self.provinceMapLocation = provinceMapLocation

    def getProvinceMapLocation(self):
        return self.provinceMapLocation

    def onMouseMapClick(self, x, y):
        print("x = {}, y = {}".format(x, y))
        sys.stdout.flush()