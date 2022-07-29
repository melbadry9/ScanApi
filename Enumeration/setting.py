from Enumeration.core.util import dir_folder, dns_folder, yaml_folder


WildDetection = True 

# tools Configuration
CHAOS = {
    "key": "",
}

SUBOVER = {
    "threads": "30",
}

GOBUSTER = {
    "threads": "30",
    "resolver": "1.1.1.1",
    "wordlist": dns_folder("small_dns.txt"),
}

AIODNSBRUTE = {
    "wordlist": dns_folder("small_dns.txt"),
}

NUCLEI_TAKEOVER = {
    "threads": "35",
    "template": yaml_folder("all-takeover.yaml"),
}

ENUM_SHODAN = {
    "key": ""
}

ENUM_GIT = {
    "key": ""
}

DNSX = {
    "wild_num": "15",
    "threads": "250"
}

DNSX_BRUTE = {
    "threads": "250",
    "wordlist": dns_folder("small_dns.txt"),
}

# Access keys and webhooks
SLACK = {
    "report_hook": ""
}

AWS = {
    "id": "",
    "secret": "",
    "upload": False,
    "upload_bucket": "",
}