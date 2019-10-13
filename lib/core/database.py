import os
import json
import sqlite3

from pathlib2 import Path
from threading import Lock
from ..paths.helper import DB_FILE


class DataBase(object):
    lock = Lock()
    def __init__(self):
        pass

class S3Data(DataBase):
    def __init__(self, bucket):
        DataBase.__init__(self)
        self.bucket = bucket

        # connect to db
        self.db = sqlite3.connect(str(DB_FILE))
        self.cdb = self.db.cursor()
        
        # Create tables 
        self.create_db()

    def __del__(self):
        self.db.close()
    
    def create_db(self):
        with self.lock:
            self.cdb.executescript("""CREATE TABLE IF NOT EXISTS `buckets` ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `bucket_name` TEXT NOT NULL, `bucket_upload` INTEGER NOT NULL, `bucket_policy` INTEGER NOT NULL, `bucket_list` INTEGER NOT NULL, `bucket_permission` INTEGER NOT NULL, `bucket_report` TEXT NOT NULL )""")
            self.db.commit()

    def insert_bucket(self, s3_):
        with self.lock:
            self.cdb.execute("insert into buckets (bucket_name, bucket_upload, bucket_policy, bucket_list, bucket_permission, bucket_report) values (?,?,?,?,?,?)",(self.bucket, s3_['bucket_upload'], s3_['bucket_policy'], s3_['bucket_list'], s3_['bucket_acl'], json.dumps(s3_['full_report'], default=str)))
            self.db.commit()

    def read_bucket(self):
        self.cdb.execute("select * from buckets where bucket_name = ?",(self.bucket,))
        db_data = self.cdb.fetchall()
        if len(db_data) == 0:
            return {} 
        return self.dictfy(db_data[0])

    @staticmethod
    def dictfy(data):
        s3_ = {}
        token = ['id', 'bucket_name', 'bucket_upload', 'bucket_policy', 'bucket_list', 'bucket_acl', 'bucket_report']
        for i in range(0,len(token)):
            if i == 6:
                s3_[token[i]] =json.loads(data[i])
            else:
                s3_[token[i]] = data[i]
        return s3_

class SubDomainData(DataBase):
    def __init__(self, domain):
        DataBase.__init__(self)
        self.domain = domain

        # connect to db
        self.db = sqlite3.connect(str(DB_FILE))
        self.cdb = self.db.cursor()
        
        # Create tables 
        self.create_db()
        
        # Get old subdomains
        self.old_sub = self.read_domains()

    def __del__(self):
        self.db.close()
    
    def create_db(self):
        with self.lock:
            self.cdb.executescript("""CREATE TABLE IF NOT EXISTS "domains" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `main_domain` TEXT NOT NULL , `sub_domain` TEXT )""")
            self.db.commit()

    def insert_domains(self, sub_domain:list):
        with self.lock:
            for item in sub_domain:
                if item not in self.old_sub:
                    self.cdb.execute("insert into domains (main_domain,sub_domain) values (?,?)",(self.domain,item))
            self.db.commit()

    def read_domains(self):
        self.cdb.execute("select sub_domain from domains where main_domain = ?",(self.domain,))
        return [i[0] for i in self.cdb.fetchall()]

    def new_domains(self):
        return list(set(self.read_domains()) - set(self.old_sub))
