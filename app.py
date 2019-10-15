import json
import multiprocessing
from flask import Flask, jsonify, render_template, Response, request

import lib.core.log_handler
from lib.core.config import config
from lib.scan.s3_job import s3_job, get_s3
from lib.scan.subdomain_job import sub_job, get_subdomains


# Init flask app
Scan = Flask(__name__)
Scan.secret_key = config["FLASK"]["secret"]

@Scan.route("/")
def index():
    return render_template("active.html")

@Scan.route("/enum/domain/<domain>/")
def Subdomain_enumeration(domain):
    multiprocessing.Process(target=sub_job, args=(domain,)).start()
    return jsonify({"status": 200})

@Scan.route("/enum/s3/<bucket>/")
def S3_check(bucket):
    process = multiprocessing.Process(target=s3_job, args=(bucket,))
    process.start()
    process.join()
    return jsonify(get_s3(bucket))

@Scan.route("/db/domain/<domain>/")
def Subdomain_from_db(domain):
    protocol = request.args.get("pro") or ""
    return Response(get_subdomains(domain, protocol),200,mimetype="text/plain")

@Scan.route("/db/s3/<bucket>/")
def s3_from_db(bucket):
    return jsonify(get_s3(bucket))

if __name__ == "__main__":
    options = config["FLASK"]
    Scan.run(host=options['host'], port=int(options['port']), debug=options.getboolean('debug'))