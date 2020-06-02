import json
import logging 
import tempfile

from ..core.utils import clean
from ..core.config import config
from ..core.slack import push_slack
from ..core.log_handler import scan_logger
from ..thirdparty.Gasset.asset import main as Gasset
from ..thirdparty.Sublist3r.sublist3r import main as Sublist3r
from ..core.opp import SubOver, GoBuster, AssetFinder, Amass, GoBusterDNS, Httprobe, Findomain, Subfinder



if config['DB']['name'] == "mysql":
    from ..core.database_mysql import SubDomainData
elif config['DB']['name'] == "sqlite3":
    from ..core.database import SubDomainData


def sub_job(domain):
    meta_data = {}
    final_list = list()
    final_error = list()
    DB = SubDomainData(domain)
    meta_data['domain'] = domain

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
            final_error.append(data['AssetFinder']['error'])
        except Exception as e:
            error_msg = "AssetFinder: " + str(e)
            scan_logger.error(error_msg, exc_info=True)
            final_error.append(error_msg)

    # Findomain
    if config['TOOLS'].getboolean('findomain'):
        try:
            pro_findomain_finder = Findomain(domain)
            data = pro_findomain_finder.exec_command()
            final_list.extend(data['Findomain']['data'])
            final_error.append(data['Findomain']['error'])
        except Exception as e:
            error_msg = "Findomain: " + str(e)
            scan_logger.error(error_msg, exc_info=True)
            final_error.append(error_msg)
    
    # Subfinder
    if config['TOOLS'].getboolean('subfinder'):
        try:
            pro_subfinder_finder = Subfinder(domain)
            data = pro_subfinder_finder.exec_command()
            final_list.extend(data['Subfinder']['data'])
            final_error.append(data['Subfinder']['error'])
        except Exception as e:
            error_msg = "Subfinder: " + str(e)
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
    meta_data['count'] = len(final_list)

     # Temp file
    temp_file = tempfile.NamedTemporaryFile("w+t", encoding="utf-8", delete=False)
    for item in final_list:
        temp_file.writelines(item + "\n")
    temp_file.seek(0)

    # SubOver
    if config['TOOLS'].getboolean('subover'):
        try:
            pro_subover = SubOver(temp_file.name)
            data = pro_subover.exec_command()
            takeover = data['SubOver']['data']
            final_error.append(data['SubOver']['error'])
            if not len(takeover) == 0:
                meta_data['takeovers'] = takeover
        except Exception as e:
            error_msg = "SubOver: " + str(e)
            scan_logger.error(error_msg, exc_info=True)
            final_error.append(error_msg)
    
    DB.insert_domains(final_list)
    new_subs = DB.new_domains()

    # Httprobe
    if config['TOOLS'].getboolean('httprobe'):
        try:
            http_probe = Httprobe(temp_file.name)
            data = http_probe.exec_command()
            alive_data = data['Httprobe']['data']
            https_domain = [dom.replace("https://","") for dom in alive_data if dom.startswith("https://")]
            http_domain = [dom.replace("http://","") for dom in alive_data if dom.startswith("http://")]
            DB.update_protocol("http", http_domain)
            DB.update_protocol("https", https_domain)
            DB.Save()
        except Exception as e:
            error_msg = "Httprobe: " + str(e)
            scan_logger.error(error_msg, exc_info=True)
            final_error.append(error_msg)

    # Bypass first run and  avoid huge host on slack webhook
    if not len(new_subs) == len(final_list):
        if not len(new_subs) == 0:
            meta_data['new_count'] = len(new_subs)
            if not len(new_subs) > 200:
                meta_data['subdomains'] = new_subs

    # Add Errors
    if len(set(final_error) - {""}) > 0:
        meta_data['errors'] = final_error

    # Slack Notification
    if config['SLACK'].getboolean('enabled'):
        push_slack(config["SLACK"]["hook"] ,json.dumps(meta_data, indent=4))
    
    # Log result
    scan_logger.info(json.dumps(meta_data, indent=4))
    return meta_data

def get_subdomains(domain, protocol):
    DB = SubDomainData(domain)
    if protocol == "http":
        subs = DB.read_domains_protocol("http")
    elif protocol == "https":
        subs = DB.read_domains_protocol("https")
    else:
        subs = DB.read_domains()
    return '\n'.join(subs)