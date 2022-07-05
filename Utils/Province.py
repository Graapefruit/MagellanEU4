class Province:
	def __init__(self, id, name, color):
		self.id = id
		self.name = name
		self.color = color
		self.pixels = []
		self.xSum = 0
		self.ySum = 0
		self.count = 0
		self.historyFile = ""

		self.cores = []
		self.owner = ""
		self.culture = ""
		self.religion = ""
		self.hre = ""
		self.tax = 1
		self.production = 1
		self.manpower = 1
		self.tradeGood = ""
		self.discovered = []

		self.area = None
		self.continent = None
		self.terrain = ""
		self.climate = None
		self.winter = None

	def addPixel(self, pixel):
		self.pixels.append(pixel)
		self.xSum += pixel.x
		self.ySum += pixel.y
		self.count += 1

	def calculateAverageX(self):
		return round(self.xSum / self.count, 3)

	def calculateAverageY(self):
		return round(self.ySum / self.count, 3)

	def __str__(self):
		return "Province {}".format(self.key)