import re
import logging
import subprocess
from threading import Thread


base_process = logging.getLogger("core.tool")
base_process.addHandler(logging.NullHandler())

class ProcessBase():
    def __init__(self, domain, errors):
        self.tool_name = None
        self.result = None
        self.domain = domain
        self.command = None
        self.pattern = None
        self.errors = errors
        
    def get_results(self):
        error = self.result[1].decode("utf-8")
        data = re.findall(self.pattern, self.result[0].decode("utf-8"))
        base_process.info("{} - Pulling {} data".format(self.domain ,self.tool_name))
        return {"error": error, "data": data}
    
    def exec(self):
        base_process.debug("{} - Running {}".format(self.domain, self.tool_name))
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.result = process.communicate()
        return self.get_results()

class BaseThreaded(Thread, ProcessBase):
    def __init__(self, domain, shared, shared_error, errors):
        ProcessBase.__init__(self, domain, errors)
        Thread.__init__(self)
        self.shared = shared
        self.shared_error = shared_error

    def run(self):
        result = self.exec()
        self.shared.extend(result['data'])
        if self.errors:
            self.shared_error.extend([result['error']])
