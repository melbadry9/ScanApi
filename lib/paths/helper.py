import os
from pathlib2 import Path

SRC_PATH =  Path.joinpath(Path(os.path.abspath(os.path.dirname(__file__))),"../")

#config
CONFIG_FILE = Path.joinpath(SRC_PATH, "../config.ini")

# Dirs bruteforce
DIR_LONG = Path.joinpath(SRC_PATH,"wordlist/long_dir.txt")
DIR_SMALL = Path.joinpath(SRC_PATH,"wordlist/small_dir.txt")
DIR_MEDIUM = Path.joinpath(SRC_PATH,"wordlist/medium_dir.txt")

# DNS bruteforce
DNS_LONG = Path.joinpath(SRC_PATH,"wordlist/long_dns.txt")
DNS_SMALL = Path.joinpath(SRC_PATH,"wordlist/small_dns.txt")
DNS_MEDUIM = Path.joinpath(SRC_PATH,"wordlist/medium_dns.txt")

# Datanbases
DB_FOLDER = Path.joinpath(SRC_PATH,"db/")
DB_FILE = Path.joinpath(DB_FOLDER,"scan.db")