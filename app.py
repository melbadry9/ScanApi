import json
import logging
import tempfile
import multiprocessing
from flask import Flask, jsonify, render_template

from lib.core.utils import clean
from lib.core.config import config
from lib.core.slack import push_slack
from lib.core.database import SubDomainData
from lib.thirdparty.Gasset.asset import main as Gasset
from lib.core.opp import SubOver, GoBuster, AssetFinder, Amass, GoBusterDNS
from lib.thirdparty.Sublist3r.sublist3r import main as Sublist3r

# Setting logging setting
logging.basicConfig(filename=config['LOGGING']['file_path'], filemode='w', format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
logging.getLogger('opp').propagate = config['LOGGING'].getboolean("opp")
logging.getLogger('slack').propagate = config['LOGGING'].getboolean("slack")
logging.getLogger('utils').propagate = config['LOGGING'].getboolean("utils")
logging.getLogger('asset').propagate = config['LOGGING'].getboolean("asset")
logging.getLogger('requests').propagate = config['LOGGING'].getboolean("requests")
logging.getLogger('urllib3').propagate = config['LOGGING'].getboolean("urllib3")


scan_logger = logging.getLogger("ScanApi")
scan_logger.addHandler(logging.NullHandler())

# Init flask app
Scan = Flask(__name__)
Scan.secret_key = config["FLASK"]["secret"]

def main(domain):
    final_list = list()
    final_error = list()
    DB = SubDomainData(domain)

    scan_logger.info("Enumerating {0} started".format(domain))

    # Sublist3r
    if config['TOOLS'].getboolean('sublist3r'):
        try:
            logging.getLogger("opp").debug("Starting Sublist3r")
            final_list.extend(Sublist3r(domain, 25, savefile=None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None))
            logging.getLogger("opp").info("Getting Sublist3r result")
        except Exception as e:
            error_msg = "Sublist3r: " + str(e)
            scan_logger.error(error_msg, exc_info=True)
            final_error.append(error_msg)
    
    # Gasset
    if config['TOOLS'].getboolean('gasset'):
        try:
            final_list.extend(Gasset(domain))
        except Exception as e:
            error_msg = "Gasset: " + str(e)
            scan_logger.error(error_msg, exc_info=True)
            final_error.append(error_msg)
    
    # AssetFinder
    if config['TOOLS'].getboolean('assetfinder'):
        try:
            pro_asset_finder = AssetFinder(domain)
            data = pro_asset_finder.exec_command()
            final_list.extend(data['AssetFinder']['data'])
            final_error.extend(data['AssetFinder']['error'])
        except Exception as e:
            error_msg = "AssetFinder: " + str(e)
            scan_logger.error(error_msg, exc_info=True)
            final_error.append(error_msg)
    
    # Amass    
    if config['TOOLS'].getboolean('amass'):

        try:
            pro_amass_finder = Amass(domain)
            data = pro_amass_finder.exec_command()
            final_list.extend(data['Amass']['data'])
        except Exception as e:
            error_msg = "Amass: " + str(e)
            scan_logger.error(error_msg, exc_info=True)
            final_error.append(error_msg)

    # GoBusterDNS
    if config['TOOLS'].getboolean('gobusterDNS'):
        try:
            brute_dns = GoBusterDNS(domain)
            data = brute_dns.exec_command()
            final_list.extend(data['GoBusterDNS']['data'])
        except Exception as e:
            error_msg = "GoBusterDns: " + str(e)
            scan_logger.error(error_msg, exc_info=True)
            final_error.append(error_msg)
        
    # All Subdomains
    final_list = clean(set(final_list))
    
    # SubOver
    if config['TOOLS'].getboolean('subover'):

        # Temp file
        temp_file = tempfile.NamedTemporaryFile("w+t", encoding="utf-8")
        for dom in final_list:
            temp_file.writelines(dom + "\n")

        try:
            pro_subover = SubOver(temp_file.name)
            data = pro_subover.exec_command()
            takeover = data['SubOver']['data']
            final_error.extend(data['SubOver']['error'])
        except Exception as e:
            error_msg = "SubOver: " + str(e)
            scan_logger.error(error_msg, exc_info=True)
            final_error.append(error_msg)

    DB.insert_domains(final_list)
    new_subs = DB.new_domains()

    #subdomains
    meta_data = {
        "domain": domain,
        "count": len(final_list),
        "new_count": len(new_subs),
        "subdomains": new_subs,
        "takeovers": takeover,
        "errors": final_error
    }
    
    # Slack Notification
    if config['SLACK'].getboolean('enabled'):
        push_slack(config["SLACK"]["hook"] ,json.dumps(meta_data, indent=4))
    
    # Log result
    scan_logger.info(json.dumps(meta_data, indent=4))
    return meta_data

@Scan.route("/")
def index():
    return render_template("active.html")

@Scan.route("/enum/<domain>/")
def Subdomain_enumeration(domain):
    multiprocessing.Process(target=main, args=(domain,)).start()
    return jsonify({"status": 200})

if __name__ == "__main__":
    options = config["FLASK"]
    Scan.run(host=options['host'], port=int(options['port']), debug=options.getboolean('debug'))