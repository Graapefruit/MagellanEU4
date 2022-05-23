class RGB:
	def __init__(self, red, green, blue):
		self.red = red
		self.green = green
		self.blue = blue

	def newFromTuple(tuple):
		return RGB(tuple[0], tuple[1], tuple[2])

	def __eq__(self, other):
		return self.red == other.red and self.green == other.green and self.blue == other.blue 

	def __str__(self):
		return "Red: {}, Green: {}, Blue: {}".format(self.red, self.green, self.blue)

	# Hash is the html representation of the number as a decimal
	def __hash__(self):
		return int(self.getHtmlColor(), base=16)

	def getHtmlColor(self):
		return self.__getColorHexString__(self.red) + self.__getColorHexString__(self.green) + self.__getColorHexString__(self.blue)

	def __getColorHexString__(self, color):
		h = hex(color)[2:]
		if len(h) == 1:
			return "0" + h
		return h