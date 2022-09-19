class Province:
	def __init__(self, id, name, color):
		self.id = id
		self.name = name
		self.color = color
		self.pixels = []
		self.historyFile = ""
		self.localizationName = name
		self.localizationAdjective = name + "er"
		self.isSea = False
		self.isLake = False

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
		self.discovered = set()

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

	def getFieldFromString(self, field):
		match field:
			case "capital":
				return self.capital
			case "religion":
				return self.religion
			case "culture":
				return self.culture
			case "tax":
				return self.tax
			case "production":
				return self.production
			case "manpower":
				return self.manpower
			case "development":
				return self.tax + self.production + self.manpower
			case "tradeGood":
				return self.tradeGood
			case "area":
				return self.area
			case "continent":
				return self.continent
			case "hre":
				return self.hre
			case "owner":
				return self.owner
			case "controller":
				return self.controller
			case "cores":
				return self.cores
			case "terrain":
				return self.terrain
			case "climate":
				return self.climate
			case "weather":
				return self.weather
			case "tradeNode":
				return self.tradeNode
			case "impassable":
				return self.impassable
			case "isSea":
				return self.isSea
			case "isLake":
				return self.isLake
			case _:
				if field in self.discovered:
					return self.discovered[field]
				else:
					print("ERROR: Field {} is unknown".format(field))
					return None

	def setFieldFromString(self, field, value):
		match field:
			case "capital":
				self.capital = value
			case "religion":
				self.religion = value
			case "culture":
				self.culture = value
			case "tax":
				if value == "":
					self.tax = 0
				else:
					self.tax = int(value)
			case "production":
				if value == "":
					self.production = 0
				else:
					self.production = int(value)
			case "manpower":
				if value == "":
					self.manpower = 0
				else:
					self.manpower = int(value)
			case "tradeGood":
				self.tradeGood = value
			case "area":
				self.area = value
			case "continent":
				self.continent = value
			case "hre":
				self.hre = (value == 1)
			case "owner":
				self.owner = value
			case "controller":
				self.controller = value
			case "cores":
				self.cores = list(map(lambda n: n.strip(), value.split(','))) if len(value.strip()) > 0 else []
			case "terrain":
				self.terrain = value
			case "climate":
				self.climate = value
			case "weather":
				self.weather = value
			case "tradeNode":
				self.tradeNode = value
			case "impassable":
				self.impassable = (value == 1)
			case "isSea":
				self.isSea = (value == 1)
			case "isLake":
				self.isLake = (value == 1)
			case _:
				if field in self.discovered:
					self.discovered[field] = value
				else:
					print("ERROR: Field {} is unknown".format(field))