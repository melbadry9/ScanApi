from Enumeration.setting import ENUM_GIT
from Enumeration.core.lib.s3 import AwsScanner
from Enumeration.core.lib.gasset import gasset
from Enumeration.core.lib.gitsub import gitsearch
from Enumeration.core.lib.sublist3r import sublister
from Enumeration.core.tool.base import BaseThreaded, base_process


class SubList3r(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "sublist3r"

    def exec(self):
        base_process.info("{} - Pulling {} data".format(self.domain ,self.tool_name))
        return {
            "error": "",
            "data": sublister(self.domain, 25, savefile=None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None),
        }

class Qenum(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "gasset"

    def exec(self):
        base_process.info("{} - Pulling {} data".format(self.domain ,self.tool_name))
        return {
            "error": "",
            "data": gasset(self.domain),
        }

class GitEnum(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "github_enum"

    def exec(self):
        base_process.info("{} - Pulling {} data".format(self.domain ,self.tool_name))
        return {
            "error": "",
            "data": gitsearch(self.domain, ENUM_GIT['key']),
        }


__dir__ = [
    Qenum,
    GitEnum,
    SubList3r,
    AwsScanner,
]