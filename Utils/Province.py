class Province:
	def __init__(self, id, capital, color):
		self.id = id
		self.capital = capital
		self.color = color
		self.pixels = []
		self.historyFile = ""

		self.localizationName = capital
		self.localizationAdjective = capital + "er"
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