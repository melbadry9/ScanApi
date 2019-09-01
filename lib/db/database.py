import os
import sqlite3

from pathlib2 import Path
from threading import Lock

from ..paths.helper import DB_FILE


class DatabaseHandler(object):
    def __init__(self):
        self.lock = Lock()
        self.db = sqlite3.connect(str(DB_FILE))
        self.cdb = self.db.cursor()
        self.CreateDB()

    def __del__(self):
        self.db.close()
    
    def CreateDB(self):
        self.cdb.executescript("""CREATE TABLE IF NOT EXISTS "scan" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `code` TEXT NOT NULL , `result` TEXT )""")
        self.cdb.executescript("""CREATE TABLE IF NOT EXISTS "gobuster" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `code` TEXT NOT NULL , `result` TEXT )""")
        self.db.commit()


    def Insert(self, domain, scan_code):
        with self.lock:
            self.cdb.execute("insert into scan (code,result) values (?,?)",(scan_code,domain))
            self.db.commit()

    def Read(self, scan_code):
        self.cdb.execute("select * from scan where code = ?",(scan_code,))
        return self.cdb.fetchall()

    def GoInsert(self, domain, scan_code):
        with self.lock:
            self.cdb.execute("insert into gobuster (code,result) values (?,?)",(scan_code,domain))
            self.db.commit()
    
    def GoRead(self, scan_code):
        self.cdb.execute("select * from gobuster where code = ?",(scan_code,))
        return self.cdb.fetchall()
