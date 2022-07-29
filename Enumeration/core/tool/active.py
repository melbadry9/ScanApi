from .base import BaseThreaded
from Enumeration.setting import GOBUSTER, AIODNSBRUTE, DNSX, DNSX_BRUTE


class GoBusterDNS(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.name = "gobuster_dns"
        self.command = "gobuster dns -z -q -d {0} -r {1} -w {2} -t {3}".format(domain, GOBUSTER['resolver'], GOBUSTER['wordlist'], GOBUSTER['threads'])
        self.pattern = r"Found: (.+)\n"

class AioDNS(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "aiodnsbrute"
        self.command = "aiodnsbrute {0} -w {1} --no-verify".format(domain, AIODNSBRUTE['wordlist'])
        self.pattern = r"0m(\S+)[\s]+\t"

class DnsxFilter(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors, file_location):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "dnsx"
        self.command = "cat {} | dnsx -wt {} -t {} -wd {} -silent".format(file_location, DNSX["wild_num"], DNSX["threads"], domain)
        self.pattern = r"(.+)\n"

class DnsxBrute(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors, file_location):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "dnsx"
        self.command = "dnsx -t {} -w {} -d {} -silent".format(DNSX_BRUTE["threads"], DNSX["wordlist"], domain)
        self.pattern = r"(.+)\n"