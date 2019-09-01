import os
from pathlib2 import Path


SRC_PATH =  Path.joinpath(Path(os.path.abspath(os.path.dirname(__file__))),"../")

#config
CONFIG = Path.joinpath(SRC_PATH, "../config.ini")

# Wordlists
LONG = Path.joinpath(SRC_PATH,"wordlist/long.txt")
MEDIUM = Path.joinpath(SRC_PATH,"wordlist/medium.txt")

# Datanbases
DB_FOLDER = Path.joinpath(SRC_PATH,"db/")
DB_FILE = Path.joinpath(DB_FOLDER,"scan.db")