import logging
import validators


utils_logger = logging.getLogger("utils")
utils_logger.addHandler(logging.NullHandler())

bad_char = ["*.", " "]

def clean(domains):
    new_domains = set()
    for dom in domains:
        dom = dom.lower()
        if not validators.domain(dom):
            old_domain = dom

            for char in bad_char:
                dom = dom.replace(char ,"")
            if validators.domain(dom):
                utils_logger.debug("Domain {0} removed reason: not valid".format(old_domain))
                new_domains.add(dom)
        else:
            new_domains.add(dom)
    return sorted(new_domains)