import re

MAP_FOLDER_NAME = "map"
LOCALIZATION_FOLDER_NAME = "localisation"
PROVINCE_FILE_NAME = "provinces.bmp"
PROVINCE_DEFINITION_FILE_NAME = "definition.csv"
DEFAULT_FILE_NAME = "default.map"
ADJACENCIES_FILE_NAME = "adjacencies.csv"
AREAS_FILE_NAME = "area.txt"
REGIONS_FILE_NAME = "region.txt"
SUPERREGIONS_FILE_NAME = "superregion.txt"
CONTINENTS_FILE_NAME = "continent.txt"
POSITIONS_FILE_NAME = "positions.txt"
TERRAIN_FILE_NAME = "terrain.txt"
PROVINCES_HISTORY_PATH = "history/provinces"
CHARACTERS_PER_LINE_CONTINENT = 25

MAP_FOLDER_NAME = "map"
RNW_PROVINCE_KEY = "RNW"

# Regex

LOCALIZATION_PATTERN = re.compile(" PROV([0-9]*):[0-9]* \"(.*)\"", re.IGNORECASE)
GROUPING_PATTERN = re.compile("([a-z_]+)\s*=\s*{([a-z0-9_\s]*)}", re.IGNORECASE)
AREA_GROUPING_PATTERN = re.compile("([a-z_]+)\s*=\s*{\s*(color\s*=\s*{\s*[0-9]{1,3}\s*[0-9]{1,3}\s*[0-9]{1,3}\s*})?([a-z0-9_\s]*)}", re.IGNORECASE)
AREA_COLOR_GROUPING_PATTERN = re.compile("color\s*=\s*{\s*([0-9]{1,3})\s*([0-9]{1,3})\s*([0-9]{1,3})\s*}")
REGION_GROUPING_PATTERN = re.compile("([a-z_]+)\s*=\s*{\s*areas\s*=\s*{([a-z0-9_\s]*)}[monsoon0-9.={}\s]*}", re.IGNORECASE) # Note that monsoons are ignored. They will have to be done manually, or add this feature in later
TERRAIN_FILE_GROUPING_PATTERN = re.compile("([a-z_]*)\s*=\s*{([\sa-z]*)color *= *{\s*([0-9]*\s*[0-9]*\s*[0-9]*)\s*}([\sa-z0-9_=.-]*)(terrain_override *= *{[\s0-9#a-z.:-_&,]*})?([\sa-z0-9_=.]*)}", re.IGNORECASE)
CONTINENT_FILE_GROUPING_PATTERN = re.compile("([a-z_]+)\s*=\s*{([a-z0-9_#\s/.&+:-]*)}", re.IGNORECASE)