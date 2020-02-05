import logging 
from .config import config


# Setting logging setting
logging.basicConfig(filename=config['LOGGING']['file_path'], filemode='w', format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

loggers = [
    'db',
    's3', 
    'opp', 
    'slack', 
    'utils', 
    'asset', 
    'requests',
    'urllib3', 
    'botocore', 
    's3transfer',
    'werkzeug'
    ]

for logger in loggers:
    logging.getLogger(logger).propagate = config['LOGGING'].getboolean(logger)

scan_logger = logging.getLogger("ScanApi")
scan_logger.addHandler(logging.NullHandler())