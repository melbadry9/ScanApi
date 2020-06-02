import logging
import MySQLdb

from ..core.config import config


database = logging.getLogger("db")
database.addHandler(logging.NullHandler())

class SubDomainData():
    def __init__(self, domain):
        self.domain = domain
        self.config = config['MYSQL']

        # connect to db
        self.db = MySQLdb.connect(self.config['host'], self.config['user'], self.config['password'], self.config['db_name'], autocommit=False)
        self.cdb = self.db.cursor()
        
        # Create tables 
        self.create_db()
        
        # Get old subdomains
        self.old_sub = self.read_domains()

    def __del__(self):
        self.db.close()

    def Save(self):
        self.db.commit()
    
    def create_db(self):
        self.cdb.execute("""
        CREATE TABLE IF NOT EXISTS `domains` (
            `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
            `main_domain` tinytext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
            `sub_domain` tinytext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
            `http` int(1) UNSIGNED NOT NULL DEFAULT 0,
            `https` int(1) UNSIGNED NOT NULL DEFAULT 0,
            PRIMARY KEY (`id`) USING BTREE,
            UNIQUE INDEX `unique`(`sub_domain`(100)) USING BTREE,
            INDEX `main_domain_index`(`main_domain`(100), `sub_domain`(100)) USING BTREE,
            INDEX `http_index`(`sub_domain`(100), `http`) USING BTREE,
            INDEX `https_index`(`sub_domain`(100), `https`) USING BTREE
            )""")
        self.Save()

    def insert_domains(self, sub_domain:list):
        for item in sub_domain:
            if item not in self.old_sub:
                try:
                    self.cdb.execute("insert ignore into domains (main_domain,sub_domain) values (%s,%s)",(self.domain,item))
                except Exception as e:
                    database.error("Error while inserting in db\n {0}".format(e), stack_info=True)
        self.Save()

    def read_domains(self):
        self.cdb.execute("select sub_domain from domains where main_domain = %s",(self.domain,))
        return [i[0] for i in self.cdb.fetchall()]

    def update_protocol(self, protocol:str, sub_domain:list):
        for item in sub_domain:
            if protocol == "http":
                self.cdb.execute("update domains set http = 1 where sub_domain=%s", (item,))
            elif protocol == "https":
                self.cdb.execute("update domains set https = 1 where sub_domain=%s", (item,))
        self.Save()

    def read_domains_protocol(self, protocol:str):
        if protocol == "http":
            self.cdb.execute("select sub_domain from domains where main_domain = %s and http=1",(self.domain,))
        elif protocol == "https":
            self.cdb.execute("select sub_domain from domains where main_domain = %s and https=1",(self.domain,))
        return [i[0] for i in self.cdb.fetchall()]
    
    def new_domains(self):
        return list(set(self.read_domains()) - set(self.old_sub))
