"""
Django settings for twinning project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMINS = ['cj@ytrychoose.com']
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5n076m!!(kjy3#q@-ub9)t!e+gye0%sj$zb274=uran18%7mg3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SITE_ID = 1
ALLOWED_HOSTS = ['api.trychoose.com','www.api.trychoose.com']


# Application definition

DEFAULT_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites'
)

THIRD_PARTY_APPS = (
    'cumulus',
)

MY_APPS = (
    'users',
    'votes',
)

INSTALLED_APPS = DEFAULT_APPS + MY_APPS + THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'users.middleware.CheckException',
)

ROOT_URLCONF = 'twinning.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/twinning/templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'twinning.wsgi.application'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/cjogbuehi/logs/choose.log',
            'formatter': 'verbose'
        },
        'mail_admins':{
            'level':'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'users': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'votes': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE':'django.db.backends.postgresql_psycopg2',
        'NAME': 'choose',
        'USER':os.environ.get('DB_USER', ''),
        'PASSWORD':os.environ.get('DB_PASS', ''),
        'HOST':'localhost'
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_COOKIE_DOMAIN =".api.trychoose.com"

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#email settings
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_USER', '')
SERVER_EMAIL = os.environ.get('EMAIL_USER', '')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS', '')

#databse performance help
CONN_MAX_AGE = 60 # tune this based on traffic

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/cjogbuehi/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

AUTH_USER_MODEL = 'users.UserProfile'

#image storage
CUMULUS = {
    'USERNAME': 'cjogbuehi',
    'API_KEY': '8f331476559e8f3c5255714ad8a1bcfd',
    'CONTAINER': 'choose-001',
    'STATIC_CONTAINER':'choose-static',
    'PYRAX_IDENTITY_TYPE': 'rackspace',
    'USE_SSL':False,
    'CNAMES':{
        'http://d4d4fa7cf0b2ba9ea99e-9f937d12f8afada8e7f4b412171af17f.r43.cf1.rackcdn.com':'http://images.trychoose.com'
    },
    'GZIP_CONTENT_TYPES':['image/jpeg','text/css','image/png'],
    'HEADERS':(
        (r'.*\.(eot|otf|woff|ttf|css|js)$', {
            'Access-Control-Allow-Origin': '*'
        }),
    )
    
}

DEFAULT_FILE_STORAGE = 'cumulus.storage.CumulusStorage'
#STATICFILES_STORAGE = 'cumulus.storage.CumulusStaticStorage'

# QuestionTypes
QUESTION_TYPE_A_B = 100
QUESTION_TYPE_YES_NO = 101

# Fake users, fake votes, fake notifications
FAKE_IT = True

#Parse api settings
APPLICATION_ID = "Jnloet4uKj9z5hJOaVdiIKRRrOzLCUf1COzse16Z"
REST_API_KEY = "3JwjuE2REL6zrAyIEjMfoDouECBFS27E5HaToZIu"
MASTER_KEY = "NZMD1EVuQ8DFbOGN8RCl6iYb1llRxD48U9hRMLQE"


try:
    from local_settings import *
except ImportError:
    pass

