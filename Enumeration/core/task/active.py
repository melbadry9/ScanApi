import logging

from Enumeration.core.task import _commit
from Enumeration.sources import ACTIVE_TOOLS
from Enumeration.core.util import check_domain


# Logging instance 
active_enum = logging.getLogger('core.task.active')
active_enum.addHandler(logging.NullHandler())

def active_domain(domain:str, commit=True):
    """ Start active scan for sub-domains """

    final_list = []
    final_error = []

    # Enumeration threads
    active_enum.info('{} - Enumeration job started'.format(domain))
    threads = [active_tool(domain, final_list, final_error, False) for active_tool in ACTIVE_TOOLS]
    for thread in threads:
        thread.start()
    for thread in threads:
        try:
            thread.join()
        except:
            pass

    # Check vaild domains and clean errors
    final_list = check_domain(set(final_list))
    clean_errors = set(final_error) - {""}

    # Push to db, aws and slack
    if commit:
        _commit(domain, final_list, clean_errors, active_enum)

    return (final_list, clean_errors)