import os
import sys
import json
import logging

import boto3
from pathlib2 import Path
from Enumeration.setting import AWS
from botocore.exceptions import ClientError


s3_logger = logging.getLogger("s3")
s3_logger.addHandler(logging.NullHandler())
upload_file =  str(Path.joinpath(Path(os.path.abspath(os.path.dirname(__file__))),"melbadry9.txt"))

class s3(object):
    def __init__(self, bucket_name, check=True):
        self.bucket_acl = 0
        self.bucket_list = 0
        self.bucket_policy = 0
        self.bucket_upload = 0
        self.bucket_acl_res = None
        self.bucket_list_res = None
        self.bucket_upload_res = None
        self.bucket_policy_res = None
        self.bucket_name = bucket_name 
        self.file_to_upload = upload_file
        self.id = AWS["id"]
        self.secret = AWS["secret"]
        self.s3_client = boto3.client('s3', aws_access_key_id=self.id, aws_secret_access_key=self.secret)
        if check == True:
            self.check()

    def ls(self):
        try:
            response = self.s3_client.list_objects(Bucket=self.bucket_name)
            self.bucket_list = 1
            self.bucket_list_res = response
        except ClientError:
            pass

    def upload(self, name="melbadry9.txt"):
        try:
            response = self.s3_client.upload_file(self.file_to_upload, self.bucket_name, name, ExtraArgs={'ACL': 'public-read','ContentType':'text/plain'})
            self.bucket_upload = 1
            self.bucket_upload_res = "Success"
        except boto3.exceptions.S3UploadFailedError:
            pass
        return response or ""

    def acl(self):
        try:
            permission = self.s3_client.get_bucket_acl(Bucket=self.bucket_name)
            self.bucket_acl = 1
            self.bucket_acl_res = permission
        except ClientError:
            pass
            
    def policy(self):
        try:
            _policy = self.s3_client.get_bucket_policy(Bucket=self.bucket_name)
            self.bucket_policy = 1
            self.bucket_policy_res = _policy
        except ClientError:
            pass
    
    def check(self):
        s3_logger.debug("Checking s3 <{0}>".format(self.bucket_name))
        try:
            self.ls()
            self.acl()
            self.upload()
            self.policy()
        except Exception:
            s3_logger.error("s3 checking faild reason: ", exc_info=True)
    
    @property
    def result(self):
        report = {
            "bucket": self.bucket_name,
            "bucket_list": self.bucket_list,
            "bucket_policy": self.bucket_policy,
            "bucket_upload": self.bucket_upload, 
            "bucket_acl": self.bucket_acl,
            "full_report": {
                    "bucket": self.bucket_name,
                    "bucket_list_res": self.bucket_list_res,
                    "bucket_policy_res": self.bucket_policy_res,
                    "bucket_upload_res": self.bucket_upload_res, 
                    "bucket_acl_res": self.bucket_acl_res
                }
            }
        return report

if __name__ == "__main__":
    try:
        buckets = [sys.argv[1]]
    except IndexError:
        buckets = sys.stdin
        if buckets.isatty():
            exit()

    for bucket in buckets:
        chk = s3(bucket.rstrip())
        print(chk.result)