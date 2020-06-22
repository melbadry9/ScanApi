import os
from ScanApi.settings import BASE_DIR


def dir_folder(name):
    return os.path.join(BASE_DIR, 'Enumeration', 'core', 'wordlist', 'dir', name)

def dns_folder(name):
    return os.path.join(BASE_DIR, 'Enumeration', 'core', 'wordlist', 'dns', name)

def yaml_folder(name):
    return os.path.join(BASE_DIR, 'Enumeration', 'core', 'wordlist', 'yaml', name)
