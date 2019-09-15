from .helper import *
from ..core.config import config


# Set wordlist
dns = config['WORDLIST']['dns']
dire = config['WORDLIST']['dir']

# Setting dir
if dire == "small":
    DIR_LIST = DIR_SMALL 
elif dire == "medium":
    DIR_LIST = DIR_MEDIUM
else:
    DIR_LIST = DIR_LONG

# setting dns
if dns == "small":
    DNS_LIST = DNS_SMALL
elif dire == "medium":
    DNS_LIST = DNS_MEDUIM
else:
    DNS_LIST = DNS_LONG