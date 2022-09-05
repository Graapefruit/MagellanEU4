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
CLIMATE_FILE_NAME = "climate.txt"
LOCALIZATION_NAME_FILE = "prov_names_l_english.yml"
LOCALIZATION_ADJECTIVE_FILE = "prov_names_adj_l_english.yml"
PROVINCES_HISTORY_PATH = "history/provinces"
COMMON_FOLDER = "common"
TECHNOLOGY_FILE = "technology.txt"
RELIGIONS_FOLDER = "religions"
CULTURES_FOLDER = "cultures"
TRADE_GOODS_FOLDER = "tradegoods"
TRADE_NODE_FOLDER = "tradenodes"
RELIGIONS_FILE = "00_religions.txt"
CULTURES_FILE = "00_cultures.txt"
TRADE_GOODS_FILE = "00_tradegoods.txt"
TRADE_NODES_FILE = "00_tradenodes.txt"

PROVINCE_CHARACTERS_PER_LINE = 85

MAP_FOLDER_NAME = "map"
RNW_PROVINCE_KEY = "RNW"

# Regex

LOCALIZATION_NAME_PATTERN = re.compile(" _PROV([0-9]+):[0-9]\s*\"(.*)?\"", re.IGNORECASE)
LOCALIZATION_ADJECTIVE_PATTERN = re.compile(" _ADJ([0-9]+):[0-9]\s*\"(.*)?\"", re.IGNORECASE)
GROUPING_PATTERN = re.compile("([a-z_]+)\s*=\s*{([a-z0-9_\s]*)}", re.IGNORECASE)
AREA_GROUPING_PATTERN = re.compile("([a-z_]+)\s*=\s*{\s*(color\s*=\s*{\s*[0-9]{1,3}\s*[0-9]{1,3}\s*[0-9]{1,3}\s*})?([a-z0-9_\s]*)}", re.IGNORECASE)
AREA_COLOR_GROUPING_PATTERN = re.compile("color\s*=\s*{\s*([0-9]{1,3})\s*([0-9]{1,3})\s*([0-9]{1,3})\s*}")
REGION_GROUPING_PATTERN = re.compile("([a-z_]+)\s*=\s*{\s*areas\s*=\s*{([a-z0-9_\s]*)}[monsoon0-9.={}\s]*}", re.IGNORECASE) # Note that monsoons are ignored. They will have to be done manually, or add this feature in later
CONTINENT_FILE_GROUPING_PATTERN = re.compile("([a-z_]+)\s*=\s*{([a-z0-9_#\s/.&+:-]*)}", re.IGNORECASE)
CLIMATE_FILE_GROUPING_PATTERN = re.compile("([a-z_]*)\s=\s{([0-9\s]*)}", re.IGNORECASE)
PROVINCE_DATE_UPDATE_GROUPING_PATTERN = re.compile("([0-9]{4}\.[0-9]{1,2}\.[0-9]{1,2})\s*=\s*({[\s\S]*)}", re.IGNORECASE)
PROVINCE_DATE_UPDATE_PATTERN = re.compile("[0-9]{4}\.[0-9]{1,2}\.[0-9]{1,2}\s*=\s*{[\s\S]*}", re.IGNORECASE)
# The bottom 4 are all scuffed and might prove buggy in the future
TECH_GROUP_GROUPING_PATTERN = re.compile("([a-z_]*) = {\s*start_level\s=\s[0-9]+", re.IGNORECASE)
RELIGIONS_GROUPING_PATTERN = re.compile("([a-z_]*)\s*=\s*{\s*color", re.IGNORECASE)
CULTURES_GROUPING_PATTERN = re.compile("([a-z_]*)\s*=\s*{\s*primary", re.IGNORECASE)
TRADE_GOODS_GROUPING_PATTERN = re.compile("([a-z_]*)\s*=\s*{\s*color", re.IGNORECASE)