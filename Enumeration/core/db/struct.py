import logging
from django.db import transaction
from Enumeration.models import Domain, Subdomain


# Logging instance 
Log_db = logging.getLogger('core.db.struct')
Log_db.addHandler(logging.NullHandler())

class SubDomainData():
    def __init__(self, domain):
        self.dom_str = domain

        # Find domain name from db or create one
        try:
            self.domain = Domain.objects.filter(name=domain).get()
        except:
            self.domain = Domain(name=domain)
            self.domain.save()
            Log_db.debug("{} - Created".format(self.dom_str))

        # Read subdomains from db
        self.new_sub = []
        self.old_sub = self.read_domains()
        
    @transaction.atomic
    def insert_domains(self, domains:list):
        """ Insert sub-domains if not exists in the db """

        self.new_sub = self.not_in_db(domains)
        to_insert_subs = [Subdomain(name=domain, domain=self.domain) for domain in self.new_sub]
        Log_db.debug("{} - Insterting subdomains".format(self.dom_str))
        with transaction.atomic():
            Subdomain.objects.bulk_create(to_insert_subs, ignore_conflicts=True)
        Log_db.info("{} - {} Subdomains inserted".format(self.dom_str, len(self.new_sub)))

    def read_domains(self):
        """ Get sub-domains from db """

        return [sub.name for sub in Subdomain.objects.filter(domain=self.domain)]

    def update_scheme(self, scheme:str, domains:list):
        """ Update http or https scheme status """

        Log_db.debug("{} - Updating live servers".format(self.dom_str))
        for domain in domains:
            tmp_sub = Subdomain.objects.filter(name=domain).get()
            if scheme == "http":
                tmp_sub.http = True
            else:
                tmp_sub.https = True
            tmp_sub.save()
        Log_db.info("{} - Live servers updated".format(self.dom_str))

    def read_domains_scheme(self, scheme:str):
        """ Get sub-domains from db with filter scheme"""

        if scheme == "http":
            return [sub.name for sub in Subdomain.objects.filter(domain=self.domain, http=True)]
        elif scheme == "https":
            return [sub.name for sub in Subdomain.objects.filter(domain=self.domain, https=True)]
        else:
            return []
    
    def not_in_db(self, domains:list):
        return list(set(domains) - set(self.old_sub))

class DomainData():
    def __init__(self, domain):
        self.dom_str = domain
        self.domain = Domain.objects.filter(name=domain)
        
    def delete_domain(self):
        db_res = self.domain.delete()
        Log_db.debug("{} - Deleted".format(self.dom_str))
        return db_res

    def info_domain(self):
        return {
            "domain": self.dom_str,
            "count": Subdomain.objects.filter(domain=self.domain.get()).count(),
            }
