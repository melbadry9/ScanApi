from .base import BaseThreaded
from Enumeration.setting import AIODNSBRUTE, DNSX, DNSX_BRUTE


class AioDNS(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "aiodnsbrute"
        self.command = "aiodnsbrute {0} -w {1} --no-verify".format(domain, AIODNSBRUTE['wordlist'])
        self.pattern = r"0m(\S+)[\s]+\t"

class DnsxBrute(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "dnsx"
        self.command = "dnsx -t {} -w {} -d {} -silent".format(DNSX_BRUTE["threads"], DNSX_BRUTE["wordlist"], domain)
        self.pattern = r"(.+)\n"

class DnsxFilter(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors, file_location):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "dnsx"
        self.command = "cat {} | dnsx -wt {} -t {} -wd {} -silent".format(file_location, DNSX["wild_num"], DNSX["threads"], domain)
        self.pattern = r"(.+)\n"

