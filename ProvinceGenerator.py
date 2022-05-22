import random
import sys
from shutil import rmtree
from os.path import exists
from os import mkdir, listdir
from nltk.corpus import words
from Utils.Province import Province
from Utils.RGB import RGB
from Utils.Pixel import Pixel

DUPLICATES_FILE_NAME = "PotentialDuplicates.txt"
PROVINCE_BMP_FILE_PATH = "map/provinces.bmp"
DEFINITIONS_FILE_PATH = "map/definition.csv"
POSITIONS_FILE_PATH = "map/positions.txt"
PROVINCE_HISTORY_PATH = "history/provinces"
PROVINCE_LOCATLIZATION_PATH = "localization/prov_names_l_english.yml"

def populateProvinces(width, height, provinceMap):
	print("Populating Provinces...")
	sys.stdout.flush()
	provinces = []
	colorToProvinces = dict()
	provinceId = 1
	allWords = words.words()
	wordsCount = len(allWords)

	for y in range(0, height):
		for x in range(0, width):
			r, g, b = provinceMap.getpixel((x, y))
			rgb = RGB(r, g, b)
			if not rgb in colorToProvinces:
				provinceName = allWords[random.randrange(wordsCount)]
				colorToProvinces[rgb] = Province(provinceId, provinceName, rgb)
				provinces.append(colorToProvinces[rgb])
				provinceId += 1
			colorToProvinces[rgb].addPixel(Pixel(x, y))
	return provinces, colorToProvinces

def overrideOrCreateFile(path):
	if (exists(path)):
		return open(path, mode='w', encoding="utf-8")
	else:
		return open(path, mode='x', encoding="utf-8")

def createPotentialDuplicatesFile(provinces, provinceMap):
	print("Creating Potential Duplicates File...")
	sys.stdout.flush()
	potentialDuplicatesFile = overrideOrCreateFile(DUPLICATES_FILE_NAME)
	for province in provinces:
		r, g, b = provinceMap.getpixel((province.calculateAverageX(), province.calculateAverageY()))
		if RGB(r, g, b) != province.color:
			potentialDuplicatesFile.write("Province: {}\nAverage: {}, {}\nColor: {}\n\t".format(province.name, province.calculateAverageX(), province.calculateAverageY(), province.color))
			for pixel in province.pixels:
				potentialDuplicatesFile.write("{}, {} |".format(pixel.x, pixel.y))
			potentialDuplicatesFile.write("\n\n")
	potentialDuplicatesFile.close()

def createPositionsFile(modPath, provinces):
	print("Creating Positions File...")
	sys.stdout.flush()
	positionsFile = overrideOrCreateFile("{}/{}".format(modPath, POSITIONS_FILE_PATH))
	for province in provinces:
		x = province.calculateAverageX()
		y = province.calculateAverageY()
		positionsFile.write("{}={{\n\tpositions={{\n\t\t{} {} {} {} {} {} {} {} {} {} {} {} {} {}\n\t}}\n\trotation={{\n\t\t0.000 0.000 0.000 0.000 0.000 0.000 0.000\n\t}}\n\theight={{\n\t\t0.000 0.000 1.000 0.000 0.000 0.000 0.000\n\t}}\n}}\n".format(province.id, x, y, x, y, x, y, x, y, x, y, x, y, x, y, x, y, x, y, x, y, x, y, x, y, x, y, x, y))

def createDefinitionsCsv(modPath, provinces):
	print("Creating definitions.csv...")
	sys.stdout.flush()
	definitionsCsv = overrideOrCreateFile("{}/{}".format(modPath, DEFINITIONS_FILE_PATH))
	definitionsCsv.write("province;red;green;blue;x;x")
	for province in provinces:
		definitionsCsv.write("\n{};{};{};{};{};x".format(province.id, province.color.red, province.color.green, province.color.blue, province.name))
	definitionsCsv.close()

def createProvinceHistoryFiles(baseGamePath, modPath, provinces):
	print("Creating Province History Files...")
	sys.stdout.flush()
	provinceCount = len(provinces)
	newProvinceHistoryPath = "{}/{}".format(modPath, PROVINCE_HISTORY_PATH)
	if exists(newProvinceHistoryPath):
		rmtree(newProvinceHistoryPath)
	mkdir(newProvinceHistoryPath)

	oldProvinceHistoryNamesList = listdir("{}/{}".format(baseGamePath, PROVINCE_HISTORY_PATH))
	oldProvinceHistoryNamesDict = dict()
	for provinceName in oldProvinceHistoryNamesList:
		# Some provinces lack a space between the id and name, and others lack a hyphen
		id = provinceName.split('-')[0].split(' ')[0]
		oldProvinceHistoryNamesDict[int(id)] = provinceName

	for i in range(0, provinceCount):
		newProvinceFileName = "{}-{}.txt".format(provinces[i].id, provinces[i].name)
		newProvinceFile = overrideOrCreateFile("{}/{}/{}".format(modPath, PROVINCE_HISTORY_PATH, newProvinceFileName))
		newProvinceFile.write("culture = atlantean\nreligion = animism\ntrade_good = livestock\nbase_tax = 1\nbase_production = 1\nbase_manpower = 1\nis_city = no")
		newProvinceFile.close()

		if (i+1) in oldProvinceHistoryNamesDict:
			oldProvinceFile = overrideOrCreateFile("{}/{}/{}".format(modPath, PROVINCE_HISTORY_PATH, oldProvinceHistoryNamesDict[i+1]))
			oldProvinceFile.write("replace_path = \"{}/{}\"".format(PROVINCE_HISTORY_PATH, newProvinceFileName))
			oldProvinceFile.close()

def createProvinceLocalizationFiles(modPath, provinces):
	print("Creating Province Localization Files...")
	sys.stdout.flush()
	provinceLocatlizationYml = overrideOrCreateFile("{}/{}".format(modPath, PROVINCE_LOCATLIZATION_PATH))
	provinceLocatlizationYml.write("l_english:")
	for province in provinces:
		provinceLocatlizationYml.write("\n PROV{}:0 \"{}\"".format(province.id, province.name))
	provinceLocatlizationYml.close()

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: ({}) (Base Game Folder) (Mod Folder)".format(sys.argv[0]))
		quit()
	baseGamePath = sys.argv[1]
	modPath = sys.argv[2]
	provinceMap = Image.open("{}/{}".format(modPath, PROVINCE_BMP_FILE_PATH))
	width, height = provinceMap.size

	provinces, colorToProvinces = populateProvinces(width, height, provinceMap)
	createPotentialDuplicatesFile(provinces, provinceMap)
	createPositionsFile(modPath, provinces)
	createDefinitionsCsv(modPath, provinces)
	createProvinceHistoryFiles(baseGamePath, modPath, provinces)
	createProvinceLocalizationFiles(modPath, provinces)