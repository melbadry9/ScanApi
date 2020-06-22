import re
import sys
import json
import html
import queue
import logging
import threading
import multiprocessing
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup as BS

from Enumeration.setting import GASSET

asset_logger = logging.getLogger('core.lib.gasset')
asset_logger.addHandler(logging.NullHandler())

#base calsses of enumeration 
class Base(object):
    def __init__(self, domain):
        self.url = ""
        self.name = ""
        self.BASE_URL =""
        self.done = False
        self.logging = True
        self.domains = list()
        self.domain = domain   
        self.proxy = {}
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Accept-Encoding': 'gzip',
            'Cookie': GASSET['fb_cookie']}
        self.fb_url = "https://developers.facebook.com/tools/debug/echo/?q={proxy_url}"
        self.adapter = requests.adapters.HTTPAdapter(5, 10, max_retries=2)
        self.CreateSession()
       
    def CreateSession(self):
        self.session = requests.Session()
        self.session.proxies = self.proxy
        self.session.headers = self.HEADERS
        self.session.mount("https://", self.adapter)
        self.session.mount("http://", self.adapter)

    def GetUrl(self, url):
        url = quote(url)
        return self.fb_url.format(proxy_url=url)

    def GetResponseHTML(self, res):
        return html.unescape(res)

    def GetResponseJSON(self, res):
        res = self.GetResponseHTML(res)
        return json.loads(BS(res,"lxml").body.text)

    def SendRequest(self):
        pass

    def HandleResponse(self):
        pass
    
    def Logic(self, url):
        retry = 0 
        done = False
        while not done:
            try:
                if self.HandleResponse(self.SendRequest(url)):
                    done = True
                else:
                    raise Exception
            except Exception:
                retry +=1
                asset_logger.debug("{0}: Retrying n.{1}".format(self.name, retry))
   
            if retry <= 5:
                pass
            else:
                asset_logger.error("{0}: Max retrying n. reached".format(self.name))
                done = True

class BaseThreaded(multiprocessing.Process, Base):
    def __init__(self, domain, shared=None):
        Base.__init__(self, domain)
        multiprocessing.Process.__init__(self)
        self.shared = shared

    def run(self):
        asset_logger.debug("{0}: Enumerating started".format(self.name))
        self.Logic(self.url)
        self.shared.extend(self.domains)
        asset_logger.debug("{0}: Enumerating finished".format(self.name))
        
#children of enumeration sites
class Crt(BaseThreaded):
    def __init__(self, domain, shared=None):
        BaseThreaded.__init__(self, domain, shared)
        self.BASE_URL = "https://crt.sh/?q=%.{domain}&dir=^&sort=1&group=icaid"
        self.url = self.BASE_URL.format(domain=domain)

    def SendRequest(self, url):
        return self.session.get(url, stream=True, timeout=50)
    
    def HandleResponse(self, res):
        sc = res.status_code 
        res = res.text
        if sc == 200:
            regex = r"<TD>([\w\d\.\-\*]+)</TD>"
            subdom = re.findall(regex, res)
            for subdomain in subdom:
                subdomain = subdomain.replace("*.","")
                self.domains.append(subdomain)
                
            self.done = True
            return True
        else:
            return False

class FDNS(BaseThreaded):
    def __init__(self, domain, shared=None):
        BaseThreaded.__init__(self, domain, shared)
        self.BASE_URL = "http://dns.bufferover.run/dns?q=.{domain}"
        self.url = self.BASE_URL.format(domain=domain)
    
    def SendRequest(self, url):
        return self.session.get(url, stream=True)
    
    def HandleResponse(self, res):
        sc = res.status_code 
        res = res.json()
        if sc == 200:
            for item in res['FDNS_A']:
                item = item.split(",")[1]
                self.domains.append(item)               
            self.done = True
            return True
        else:
            return False

class Censys(BaseThreaded):
    Q = queue.Queue()
    def __init__(self, domain, shared=None):
        BaseThreaded.__init__(self, domain, shared)
        self.BASE_URL = 'https://censys.io/certificates/_search?q={domain}&page={page}'
        
    def Logic(self, _):
        #asset_logger.debug("{0}: Enumerating started".format(self.name))
        for i in range(1,41):
            url = self.BASE_URL.format(domain=self.domain,page=str(i))
            url = self.GetUrl(url)
            self.Q.put(threading.Thread(target=self.SendRequest, args=(url,)))
        
        while not self.Q.empty():
            th = self.Q.get()
            th.start()

        self.Q.join()
        #asset_logger.debug("{0}: Enumerating finished".format(self.name))
        
    def SendRequest(self, url):
        done = False
        while not done:
            try:
                res = self.session.get(url)
                if res.status_code == 200:
                    self.ExtractDomains(res.text)
                    done = True
            except Exception:
                asset_logger.error("{0}: ".format(self.name), exc_info=True)
        self.Q.task_done()

    def ExtractDomains(self, txt):
        txt = self.GetResponseHTML(txt)
        scraped = re.findall(r"parsed.names: ([\w\.\-]+)<mark>([\-\w\.]+)",txt)
        for scrap in scraped:
            sdomain = self.Concat(scrap).lower()
            self.domains.append(sdomain)
            
    def Concat(self, re):
        return re[0] + re[1]

class VirusTotal(BaseThreaded):
    def __init__(self, domain, shared=None):
        BaseThreaded.__init__(self, domain, shared)
        self.BASE_URL = 'https://www.virustotal.com/ui/domains/{domain}/subdomains?limit=40'
        self.url = self.BASE_URL.format(domain=domain)
        self.url = self.GetUrl(self.url)

    def SendRequest(self, url):
        return self.session.get(url)
    
    def HandleResponse(self, res):
        sc = res.status_code
        js = self.GetResponseJSON(res.text)
        
        if sc == 200:
            try:
                next_url = js['links']['next']
            except KeyError:
                next_url = None
                self.done = True
            
            if next_url:
                next_url = self.GetUrl(next_url)
                self.Logic(next_url)

            for dom in js['data']:
                self.domains.append(dom['id'])
            return True
        else:
            return False

class CertSpotter(BaseThreaded):
    def __init__(self, domain, shared=None):
        BaseThreaded.__init__(self, domain, shared)
        self.BASE_URL = "https://api.certspotter.com/v1/issuances?domain={domain}&expand=dns_names&include_subdomains=true"
        self.url = self.BASE_URL.format(domain=domain)
    
    def SendRequest(self, url):
        return self.session.get(url)
    
    def HandleResponse(self, res):
        sc = res.status_code 
        res = res.json()
        if sc == 200:
            for item in res:
                for subdomain in item['dns_names']:
                    if (not subdomain.startswith("*")) and (self.domain in subdomain):
                        self.domains.append(subdomain)                    
            self.done = True
            return True
        else:
            return False

def main(domain):
    subdomains_final = multiprocessing.Manager().list()
    
    if not GASSET['fb_cookie'] == "":
        active_resources = [Crt, FDNS, VirusTotal, CertSpotter, Censys]
    else:
        asset_logger.error("Facebook cookies not found ignoring Censys, VirusTotal")
        active_resources = [Crt, FDNS, CertSpotter]

    threads = [resource(domain, subdomains_final) for resource in active_resources]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
    subdomains_final = sorted(set(subdomains_final))
    #for sub in subdomains_final:
    #    print(sub)
    
    return subdomains_final

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        pass