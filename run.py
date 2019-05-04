import re
import os
import sys
import time
import json
import threading
import subprocess
from pathlib2 import Path
from flask import Flask, jsonify, url_for

from Core.db import DatabaseHandler
from Core.vtotal_censys import PLUS
from sublist3r.sublist3r import main as SubList


THREADS = 50
SRC_PATH =  Path(os.path.abspath(os.path.dirname(__file__)))
SUBOVER = Path.joinpath(SRC_PATH,"subover")
SUBOVER_EXE = Path.joinpath(SUBOVER,"subover")

Scan = Flask(__name__)
Scan.secret_key = "anything_12456547_1524556"

def sub(domain):
    #sublist3r enurmation
    return SubList(domain, THREADS, savefile=None, ports=None, silent=False, verbose=True, enable_bruteforce=False, engines=None)

def plu(domain):
    #virustotal and censys
    return PLUS(domain)

def subover(file):
    #subover check
    print("[-] started subover")
    pat = r"\[31\;1\;4m(\D+)\u001b\[0m\] Takeover Possible At (\S+)"
    command = "{0} -t 50 -a -l {1}".format(SUBOVER_EXE, file)
    proc2 = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = proc2.communicate()
    takeover = re.findall(pat,result[0].decode("utf-8"))
    error = result[1].decode("utf-8")
    return {"takeover": [[list(i) for i in takeover]], "errors":error}
    
def main(domain,code):
    start = time.time()
    final_list = list() 
    DB = DatabaseHandler()

    sub_domains = sub(domain)
    try:
        plus_domains = plu(domain)
    except:
        plus_domains = ["faild.tor"]

    #avoid dubplicated domains
    for dom in sub_domains:
        final_list.append(dom.lower())

    #add both domains without repeat
    for dom2 in plus_domains:
        if dom2 not in final_list:
            final_list.append(dom2)

    end = time.time()

    #write list of domains
    file_name = "{0}.txt".format(code)
    with open(file_name, "a") as e:
        for i in final_list:
            e.write(i+"\n")
    
    #takeovers
    take_over = subover(file_name)
    take_over['time'] = time.time() - end

    #subdomains
    fin = {
        "count": len(final_list),
        "subdomains": final_list,
        "time": end - start
        }

    d = json.dumps({
        "code": code,
        "domain": domain ,
        "sublist3r&plus": fin,
        "subOver": take_over ,
        })

    DB.Insert(d, code)


@Scan.route("/<domain>/<code>")
def test(domain,code):
    threading.Thread(target=main, args=(domain,code)).start()
    return jsonify({"status":"running","result_code": code})

@Scan.route("/r/<code>")
def test2(code):
    final_data = []
    DB = DatabaseHandler()

    data = [list(i) for i in DB.Read(code)]

    for item in data:
        final_data.append(json.loads(item[2]))

    return jsonify(final_data)

if __name__ == "__main__":
    Scan.run()