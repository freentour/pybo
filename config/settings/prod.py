import environ
from .base import *

ALLOWED_HOSTS = ['3rdx.2woo.net']
DEBUG = False

env = environ.Env()
env.read_env(BASE_DIR / '.env')


# MySQL Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': '3306',
    }
}


# PostgreSQL
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': '5432',
    }
}
'''


# STATIC_ROOT = BASE_DIR / 'static/'
# STATICFILES_DIRS = []


# allauth를 위한 SITE_ID for MySQL
SITE_ID = 4

'''
# allauth를 위한 SITE_ID for PostgreSQL
SITE_ID = 5
'''
