class Province:
	def __init__(self, id, name, color):
		self.id = id
		self.name = name
		self.color = color
		self.pixels = []
		self.historyFile = ""
		self.localizationName = name
		self.localizationAdjective = name + "er"

		self.capital = name
		self.cores = []
		self.owner = ""
		self.controller = ""
		self.culture = ""
		self.religion = ""
		self.hre = False
		self.tax = 1
		self.production = 1
		self.manpower = 1
		self.tradeGood = ""
		self.tradeNode = ""
		self.discovered = []

		self.area = ""
		self.continent = ""
		self.terrain = ""
		self.climate = ""
		self.weather = ""
		self.impassable = False

		self.extraText = ""
		self.provinceUpdates = []

	def __str__(self):
		return "Province {}".format(self.key)