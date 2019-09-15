import os
import sqlite3

from pathlib2 import Path
from threading import Lock

from ..paths.helper import DB_FILE


class SubDomainData(object):
    lock = Lock()
    def __init__(self, domain):
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
