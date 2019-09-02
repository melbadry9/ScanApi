import json
import logging
import tempfile
import configparser
import multiprocessing
from flask import Flask, jsonify, render_template

from lib.paths.helper import CONFIG
from lib.core.slack import push_slack
from lib.db.database import DatabaseHandler
from lib.thirdparty.Gasset.asset import main as Gasset
from lib.core.opp import SubOver, GoBuster, AssetFinder, Amass
from lib.thirdparty.Sublist3r.sublist3r import main as Sublist3r


logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)
logging.getLogger('requests').propagate = False
logging.getLogger('urllib3').propagate = False

config = configparser.ConfigParser()
config.read(str(CONFIG))

Scan = Flask(__name__)
Scan.secret_key = config["FLASK"]["secret"]

def main(domain):
    final_error = list()
    final_list = list()
    temp_file = tempfile.NamedTemporaryFile("w+t", encoding="utf-8")
    
    # Sublist3r
    try:
        final_list.extend(Sublist3r(domain, 25, savefile=None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None))
    except Exception as e:
        final_error.append("Sublist3r: " + str(e))
    
    # Gasset
    try:
        final_list.extend(Gasset(domain))
    except Exception as ee:
        final_error.append("Gasset: " + str(ee))

    # AssetFinder
    try:
        pro_asset_finder = AssetFinder(domain)
        data = pro_asset_finder.exec_command()
        final_list.extend(data['AssetFinder']['data'])
        final_error.extend(data['AssetFinder']['error'])
    except Exception as eee:
        final_error.append("AssetFinder: " + str(eee))

    #Amass
    try:
        pro_amass_finder = Amass(domain)
        data = pro_amass_finder.exec_command()
        final_list.extend(data['Amass']['data'])
    except Exception as eeee:
        final_error.append("Amass: " + str(eeee))

    # All Subdomains
    final_list = sorted(set(final_list))
    for dom in final_list:
        temp_file.writelines(dom + "\n")
    
    # SubOver
    try:
        pro_subover = SubOver(temp_file.name)
        data = pro_subover.exec_command()
        takeover = data['SubOver']['data']
        final_error.extend(data['SubOver']['error'])
    except Exception as eeeee:
        final_error.append("SubOver: " + str(eeeee))

    #subdomains
    meta_data = {
        "count": len(final_list),
        "subdomains": final_list,
        "takeovers": takeover,
        "errors": final_error
    }
    
    # Slack Notification
    push_slack(config["SLACK"]["hook"] ,json.dumps(meta_data, indent=4))
    return meta_data

@Scan.route("/")
def index():
    return render_template("active.html")

@Scan.route("/enum/<domain>/")
def Subdomain_enumeration(domain):
    multiprocessing.Process(target=main, args=(domain,)).start()
    return jsonify({"status": 200})

if __name__ == "__main__":
    Scan.run("0.0.0.0", debug=False)