from Enumeration.core.util import dir_folder, dns_folder, yaml_folder


WildDetection = False 

# tools Configuration
SHODAN_API_KEY = ""

CHAOS = {
    "key": "",
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
