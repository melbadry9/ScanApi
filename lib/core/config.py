import configparser
from ..paths.helper import CONFIG_FILE

# Parsing setting
config = configparser.RawConfigParser()
config.read(str(CONFIG_FILE))