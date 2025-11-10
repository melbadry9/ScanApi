from Enumeration.core.db import SubDomainData


def _commit(domain, subdomains:set, errors:set, logger):
    DB = SubDomainData(domain)
    DB.insert_domains(subdomains)
    logger.info('{} - Enumeration job finished'.format(domain))
    if len(errors) > 0:
        logger.error('{} - Enumeration errors: {}'.format(domain, errors))