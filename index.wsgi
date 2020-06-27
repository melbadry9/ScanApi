import os
import sys

sys.path.append('/var/www/scanapi')        
sys.path.append('/var/www/scanapi/ScanApi')

os.environ['DJANGO_SETTINGS_MODULE'] = 'ScanApi.settings'

from django.core.wsgi import get_wsgi_application        
application = get_wsgi_application()