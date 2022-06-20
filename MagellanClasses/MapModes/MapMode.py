class MapMode():
    def __init__(self):
        self.model = None
        self.image = None

    def getName(self):
        return "Abstract_MapMode"

    def setNewModel(self, model):
        self.model = model
        self.image = None

    def getOrLoadImage(self):
        pass