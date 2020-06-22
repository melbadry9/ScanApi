from .base import BaseThreaded
from Enumeration.setting import SUBOVER, NUCLEI_TAKEOVER


class SubOver(BaseThreaded):
    def __init__(self, file, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.name = "subover"
        self.command = "subover -t {0} -l {1} -a".format(SUBOVER['threads'], file)
        self.pattern = r"\[31\;1\;4m(\D+)\u001b\[0m\] Takeover Possible At (\S+)"

class NucleiTakeover(BaseThreaded):
    def __init__(self, file, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.name = "nuclei_takeover"
        self.command = "nuclei -l {0} -t {1} -c {2} -silent -nC".format(file, NUCLEI_TAKEOVER['template_file'], NUCLEI_TAKEOVER['threads'])
        self.pattern = r"\[\S+:(\S+)\]+ \[\S+\]+ (.+)\n"
