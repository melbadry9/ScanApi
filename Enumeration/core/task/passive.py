import logging 
from Enumeration.core.task import _commit
from Enumeration.setting import WildDetection
from Enumeration.sources import PASSIVE_TOOLS, WILD_TOOLS
from Enumeration.core.util import check_domain, prevent_attack, temp_file

# Logging instance 
passive_enum = logging.getLogger('core.task.passive')
passive_enum.addHandler(logging.NullHandler())

def passive_domain(domain:str, commit=True):
    """ Start passive scan for sub-domains """
    domain_safe = prevent_attack(domain)

    if domain_safe:
        final_list = []
        final_error = []
        filtered_list = []

        # Enumeration threads
        passive_enum.info('{} - Enumeration job started'.format(domain_safe))
        threads = [active_tool(domain_safe, final_list, final_error, False) for active_tool in PASSIVE_TOOLS]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # Check vaild domains
        final_list = check_domain(final_list)
        clean_errors = set(final_error) - {""}

        if WildDetection:
            file_location = temp_file(final_list)
        
            threads = [wild_tool(domain_safe, filtered_list, final_error, True, file_location) for wild_tool in WILD_TOOLS]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            final_list = set(filtered_list)

        # Push to db, aws and slack
        if commit:
            _commit(domain_safe, final_list, clean_errors, passive_enum)
        
        return (final_list, clean_errors)
    else:
        passive_enum.error('{} - Not a valid domain'.format(domain))
        return None

