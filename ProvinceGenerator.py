import random
import sys
import re
from shutil import rmtree
from os.path import exists
from os import mkdir, listdir
from nltk.corpus import words
from Utils.Province import Province
from Utils.RGB import RGB
from Utils.Pixel import Pixel
from PIL import Image
from MagellanClasses.Constants import LOCALIZATION_PATTERN

DUPLICATES_FILE_NAME = "PotentialDuplicates.txt"
PROVINCE_BMP_FILE_PATH = "map/provinces.bmp"
DEFINITIONS_FILE_PATH = "map/definition.csv"
POSITIONS_FILE_PATH = "map/positions.txt"
HISTORY_PATH = "history"
PROVINCE_HISTORY_PATH = "history/provinces"
LOCALIZATION_PATH = "localisation"
PROVINCE_LOCATLIZATION_PATH = "localisation/prov_names_l_english.yml"
PROVINCE_LOCATLIZATION_ADJ_PATH = "localisation/prov_names_adj_l_english.yml"

def populateExistingDefinitions(modPath):
	print("Populating Existing Provinces...")
	sys.stdout.flush()
	provinces = []
	colorToProvinceMap = dict()
	definitionFileLocation = "{}/{}".format(modPath, DEFINITIONS_FILE_PATH)
	localisationFileLocation = "{}/{}".format(modPath, PROVINCE_LOCATLIZATION_PATH)
	if (exists(definitionFileLocation)):
		f = open(definitionFileLocation, mode='r', encoding="utf-8")
		for line in f:
			lineData = line.split(';')
			# Ignore first line
			if lineData[0] == "province":
				continue
			rgb = RGB(int(lineData[1]), int(lineData[2]), int(lineData[3]))
			newProvince = Province(int(lineData[0]), lineData[4], rgb)
			newProvince.isNew = False
			provinces.append(newProvince)
			colorToProvinceMap[rgb] = newProvince
		f.close()

		if (exists(localisationFileLocation)):
			f = open(localisationFileLocation, mode='r', encoding="utf-8")
			matches = LOCALIZATION_PATTERN.findall(line)
			for match in matches:
				provinceId = match[0]
				provinceName = match[1]
				provinces[provinceId].name = provinceName
				
	return provinces, colorToProvinceMap

def populateNewProvinces(provinces, colorToProvinceMap, provinceMap):
	print("Populating New Provinces...")
	sys.stdout.flush()
	width, height = provinceMap.size
	nextProvinceId = len(provinces) + 1
	allWords = words.words()
	wordsCount = len(allWords)

	for y in range(0, height):
		for x in range(0, width):
			r, g, b = provinceMap.getpixel((x, y))
			rgb = RGB(r, g, b)
			if not rgb in colorToProvinceMap:
				provinceName = allWords[random.randrange(wordsCount)]
				newProvince = Province(nextProvinceId, provinceName, rgb)
				newProvince.isNew = True
				colorToProvinceMap[rgb] = newProvince
				provinces.append(newProvince)
				nextProvinceId += 1
			colorToProvinceMap[rgb].addPixel(Pixel(x, y))
	return provinces

def createExceptionsFile(provinces, provinceMap):
	print("Creating Exceptions File...")
	sys.stdout.flush()
	potentialDuplicatesFile = overrideOrCreateFile(DUPLICATES_FILE_NAME)
	for province in provinces:
		# provinces not having any pixels
		if province.count == 0:
			potentialDuplicatesFile.write("Province {}:{} has no pixels!".format(province.id, province.name))

		# provinces not containing their own center pixel (tests for two provinces using the same color: many false positives)
		else:
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
	createFolderIfNotExisting("{}/{}".format(modPath, HISTORY_PATH))
	createFolderIfNotExisting("{}/{}".format(modPath, PROVINCE_HISTORY_PATH))

	oldProvinceHistoryNamesList = listdir("{}/{}".format(baseGamePath, PROVINCE_HISTORY_PATH))
	oldProvinceHistoryNamesDict = dict()
	for provinceName in oldProvinceHistoryNamesList:
		# Some provinces lack a space between the id and name, and others lack a hyphen
		id = provinceName.split('-')[0].split(' ')[0]
		oldProvinceHistoryNamesDict[int(id)] = provinceName

	for i in range(0, provinceCount):
		if provinces[i].isNew:
			provinceFileName = ""
			if (i+1) in oldProvinceHistoryNamesDict:
				provinceFileName = oldProvinceHistoryNamesDict[i+1]
			else:
				provinceFileName = "{}-{}.txt".format(provinces[i].id, "Antarctica{}".format(provinces[i+1].id))
			provinceFile = overrideOrCreateFile("{}/{}/{}".format(modPath, PROVINCE_HISTORY_PATH, provinceFileName))
			provinceFile.write("culture = atlantean\nreligion = animism\ntrade_good = livestock\nbase_tax = 1\nbase_production = 1\nbase_manpower = 1\nis_city = no")
			provinceFile.close()

def createProvinceLocalizationFiles(modPath, provinces):
	print("Creating Province Localization Files...")
	sys.stdout.flush()
	createFolderIfNotExisting("{}/{}".format(modPath, LOCALIZATION_PATH))
	provinceLocalizationFile = overrideOrCreateFile("{}/{}".format(modPath, PROVINCE_LOCATLIZATION_PATH))
	provinceLocalizationFile.write("l_english:")
	provinceLocalizationAdjFile = overrideOrCreateFile("{}/{}".format(modPath, PROVINCE_LOCATLIZATION_ADJ_PATH))
	provinceLocalizationAdjFile.write("l_english:")
	for province in provinces:
		provinceLocalizationFile.write("\n PROV{}:0 \"{}\"".format(province.id, province.name))
		provinceLocalizationAdjFile.write("\n _ADJ{}:0 \"{}\"".format(province.id, province.name + "r"))
	provinceLocalizationFile.close()

	# --- Helpers --- #

def overrideOrCreateFile(path):
	if (exists(path)):
		return open(path, mode='w', encoding="utf-8")
	else:
		return open(path, mode='x', encoding="utf-8")

def createFolderIfNotExisting(path):
	if not exists(path):
		mkdir(path)

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Usage: ({}) (Base Game Folder) (Mod Folder)".format(sys.argv[0]))
		quit()
	baseGamePath = sys.argv[1]
	modPath = sys.argv[2]
	provinceMap = Image.open("{}/{}".format(modPath, PROVINCE_BMP_FILE_PATH))

	provinces, colorToProvinceMap = populateExistingDefinitions(modPath)
	provinces = populateNewProvinces(provinces, colorToProvinceMap, provinceMap)
	createExceptionsFile(provinces, provinceMap)
	createPositionsFile(modPath, provinces)
	createDefinitionsCsv(modPath, provinces)
	createProvinceHistoryFiles(baseGamePath, modPath, provinces)
	createProvinceLocalizationFiles(modPath, provinces)