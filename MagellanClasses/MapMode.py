class MapMode():
    def __init__(self, name, initializationFunction):
        self.name = name
        self.initializationFunction = initializationFunction
        self.image = None

    def getOrLoadImage(self):
        if not self.image:
            self.image = self.initializationFunction()
        return self.image