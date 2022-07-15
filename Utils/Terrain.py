from tracemalloc import start


class Terrain:
    def __init__(self, name, color, startText, middleText, endText):
        self.name = name
        self.color = color
        self.startText = startText
        self.middleText = middleText
        self.endText = endText