from .base import *

ALLOWED_HOSTS = ['3rdx.2woo.net']
DEBUG = False

STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []

# allauth를 위한 SITE_ID
SITE_ID = 3
