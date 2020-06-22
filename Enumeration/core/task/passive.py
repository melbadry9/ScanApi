import json
import logging 

from Enumeration.core.task import _commit
from Enumeration.sources import PASSIVE_TOOLS
from Enumeration.core.util import check_domain

# Logging instance 
passive_enum = logging.getLogger('core.task.passive')
passive_enum.addHandler(logging.NullHandler())

def passive_domain(domain:str, commit=True):
    """ Start passive scan for sub-domains """

    final_list = []
    final_error = []

    # Enumeration threads
    passive_enum.info('{} - Enumeration job started'.format(domain))
    threads = [active_tool(domain, final_list, final_error, False) for active_tool in PASSIVE_TOOLS]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    # Check vaild domains
    final_list = check_domain(set(final_list))
    clean_errors = set(final_error) - {""}

    # Push to db, aws and slack
    if commit:
        _commit(domain, final_list, clean_errors, passive_enum)
    
    return (final_list, clean_errors)
