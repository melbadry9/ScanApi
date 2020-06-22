#!/usr/bin/python3
import re
import requests
from functools import partial
from concurrent.futures import ThreadPoolExecutor


t_history = set()
t_history_urls = set()
session = requests.Session()
connection_pool = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=2)
session.mount("https://", connection_pool)
session.mount("http://", connection_pool)

def githubApiSearchCode(search, page, token):
    headers = {"Authorization": "token " + token}
    done = False
    while not done:
        url = 'https://api.github.com/search/code?s=indexed&type=Code&o=desc&q=' + search + '&page=' + str(page)
        r = session.get(url, headers=headers, timeout=2)
        if r.status_code == 200:
            json = r.json()
            done = True
    return json

def getRawUrl(result):
    raw_url = result['html_url']
    raw_url = raw_url.replace('https://github.com/','https://raw.githubusercontent.com/')
    raw_url = raw_url.replace('/blob/', '/')
    return raw_url

def readCode(domain_regexp, source, result):
    url = getRawUrl(result)
    if url in t_history_urls:
        return
    t_history_urls.add(url)

    code = doGetCode(url)
    if code:
        matches = re.findall(domain_regexp, code, re.IGNORECASE)
        if matches:
            for sub in matches:
                sub = sub[0].replace('2F', '').lower().strip()
                if len(sub):
                    t_history.add(sub)

def doGetCode(url):
    try:
        r = session.get(url, timeout=2)
    except:
        return False
    return r.text

def scan(domain, token, page):
    _search = "{0}".format(domain)
    try:
        t_json = githubApiSearchCode(_search, page, token)
        domain_regexp = r'(([0-9a-z_\-\.]+)\.' + domain.replace('.', '\.')+')'   
        Pool = ThreadPoolExecutor(max_workers=20)
        Pool.map(partial(readCode, domain_regexp, ""), t_json['items'])
        Pool.shutdown(wait=True)
    except:
        pass

def main(domain, token):
    Scan = ThreadPoolExecutor(max_workers=2)
    Scan.map(partial(scan, domain, token), [i for i in range(1,34)])
    Scan.shutdown(wait=True)
    return list(t_history)
