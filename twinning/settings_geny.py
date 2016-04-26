from settings import *

SITE_ID = 4
ALLOWED_HOSTS = ['genysolutions.co','www.genysolutions.co']

ROOT_URLCONF = 'twinning.urls_geny'

try:
    from local_settings import *
except ImportError:
    pass
