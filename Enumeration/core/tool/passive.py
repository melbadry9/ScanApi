from .base import BaseThreaded
from Enumeration.setting import CHAOS, ENUM_SHODAN


class AssetFinder(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "assetfinder"
        self.command = "assetfinder -subs-only {0}".format(domain)
        self.pattern = r"(.+)\n"

class Amass(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "amass"
        self.command = "amass enum -passive -d {0}".format(domain)
        self.pattern = r"(.+)\n"   

class Findomain(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "findomain"
        self.command = "findomain -t {0} -q".format(domain)
        self.pattern = r"(.+)\n"     

class Subfinder(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "subfinder"
        self.command = "subfinder -d {0} -silent".format(domain)
        self.pattern = r"(.+)\n"    

class Chaos(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "chaos"
        self.command = "chaos -silent -d {0} -key {1} ".format(domain, CHAOS['key'])
        self.pattern = r"(.+)\n"
        
class EnumShodan(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "shodan_enum"
        self.command = "enumsho -d {0} -s {1}".format(domain, ENUM_SHODAN['key'])
        self.pattern = r"(.+)\n"