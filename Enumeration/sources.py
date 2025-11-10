from Enumeration.core.lib import SubList3r, RiftEnum
from Enumeration.core.tool import Amass, AssetFinder, Findomain, Chaos, Subfinder, AioDNS, DnsxFilter, DnsxBrute


PASSIVE_TOOLS = [
    Chaos,
    Amass,
    SubList3r,
    Findomain,
    Subfinder,
    AssetFinder,
    RiftEnum
]

ACTIVE_TOOLS = [
    #AioDNS,
    DnsxBrute,
]

WILD_TOOLS = [
    DnsxFilter
]