from Enumeration.core.lib import SubList3r, Qenum, GitEnum
from Enumeration.core.tool import Amass, AssetFinder, Findomain, Chaos, Subfinder, EnumShodan, AioDNS, GoBusterDNS


PASSIVE_TOOLS = [
    #Qenum,
    Chaos,
    Amass,
    GitEnum,
    SubList3r,
    Findomain,
    Subfinder,
    AssetFinder,
    EnumShodan,
]

ACTIVE_TOOLS = [
    AioDNS,
    #GoBusterDNS,
]