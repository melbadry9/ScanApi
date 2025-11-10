from .base import BaseThreaded
from Enumeration.setting import NUCLEI_TAKEOVER

class NucleiTakeover(BaseThreaded):
    def __init__(self, file, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.name = "nuclei_takeover"
        self.command = "nuclei -l {0} -t {1} -c {2} -silent -nC".format(file, NUCLEI_TAKEOVER['template_file'], NUCLEI_TAKEOVER['threads'])
        self.pattern = r"\[\S+:(\S+)\]+ \[\S+\]+ (.+)\n"
