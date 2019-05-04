import os
import sqlite3

from pathlib2 import Path
from threading import Lock

SRC_PATH = Path.joinpath(Path(os.path.abspath(os.path.dirname(__file__))),"../")

class DatabaseHandler(object):
    def __init__(self):
        self.lock = Lock
        self.db = sqlite3.connect(str(Path.joinpath(SRC_PATH,"scan.db")))
        self.cdb = self.db.cursor()
        self.CreateDB()

    def __del__(self):
        self.db.close()
    
    def CreateDB(self):
        #with self.lock():
        self.cdb.executescript("""CREATE TABLE IF NOT EXISTS "scan" ( `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, `code` TEXT NOT NULL , `result` TEXT )""")
        self.db.commit()


    def Insert(self, domain, scan_code):
        #with self.lock():
        self.cdb.execute("insert into scan (code,result) values (?,?)",(scan_code,domain))
        self.db.commit()

    def Read(self, scan_code):
        self.cdb.execute("select * from scan where code = ?",(scan_code,))
        return self.cdb.fetchall()
