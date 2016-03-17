from settings import *

SITE_ID = 2
ALLOWED_HOSTS = ['emekaenterprises.com','www.emekaenterprises.com']

ROOT_URLCONF = 'twinning.urls_emeka'

try:
    from local_settings import *
except ImportError:
    pass
