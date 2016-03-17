from settings import *

SITE_ID = 3
ALLOWED_HOSTS = ['teamdestinyfoundation.com','www.teamdestinyfoundation.com']

ROOT_URLCONF = 'twinning.urls_destiny'

try:
    from local_settings import *
except ImportError:
    pass
