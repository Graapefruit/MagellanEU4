from tracemalloc import start


class Terrain:
    def __init__(self, name, color, provinces, startText, middleText, endText):
        self.name = name
        self.color = color
        self.provinces = provinces
        self.startText = startText
        self.middleText = middleText
        self.endText = endText