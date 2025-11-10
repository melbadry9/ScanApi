from Enumeration.core.lib.rift.rift import rift_main
from Enumeration.core.lib.sublist3r import sublister
from Enumeration.core.tool.base import BaseThreaded, base_process


class SubList3r(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "sublist3r"

    def exec(self):
        base_process.info("{} - Pulling {} data".format(self.domain ,self.tool_name))
        try:
            data = sublister(self.domain, 25, savefile=None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
            return{
            "error": "",
            "data": data
            }
        except Exception as e:
            return{
            "error": f"SubList3r:{str(e)}",
            "data": []
            }

class RiftEnum(BaseThreaded):
    def __init__(self, domain, shared, shared_error, errors):
        BaseThreaded.__init__(self, domain, shared, shared_error, errors)
        self.tool_name = "rift"

    def exec(self):
        base_process.info("{} - Pulling {} data".format(self.domain ,self.tool_name))
        try:
            data = rift_main(self.domain)
            return{
            "error": "",
            "data": list(data)
            }
        except Exception as e:
            return{
            "error": f"RiftEnum:{str(e)}",
            "data": []
            }


__dir__ = [
    SubList3r,
    RiftEnum
]