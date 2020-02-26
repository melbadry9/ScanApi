import json
import logging 
import tempfile

from ..core.config import config
from ..core.opp import SubOver
from ..core.slack import push_slack
from ..core.database import SubDomainData


takeover_logger = logging.getLogger("takeover")
takeover_logger.addHandler(logging.NullHandler())

def takeover(domain):
    result = {}
    result['domain'] = domain
    DB = SubDomainData(domain)
    domains_list = DB.old_sub

    if len(domains_list) != 0:
        takeover_logger.info("Scanning {0} for takeover".format(domain))
        # Temp file
        temp_file = tempfile.NamedTemporaryFile("w+t", encoding="utf-8", delete=False)
        for item in domains_list:
            temp_file.writelines(item + "\n")
        temp_file.seek(0)

        pro_subover = SubOver(temp_file.name)
        data = pro_subover.exec_command()
        takeover = data['SubOver']['data']
        if not len(takeover) == 0:
            result['takeovers'] = takeover
        takeover_logger.info(json.dumps(result, indent=4))
    else:
        takeover_logger.error("No domains in db for {0}".format(domain))
        result['error'] = "No Domains for {0}".format(domain)
    
    if config['SLACK'].getboolean('enabled'):
            push_slack(config["SLACK"]["takeover_hook"] ,json.dumps(result, indent=4))