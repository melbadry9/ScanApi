from Enumeration.core.util import dir_folder, dns_folder, yaml_folder


# tools Configuration
GASSET = {
    "fb_cookie": ""
}

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