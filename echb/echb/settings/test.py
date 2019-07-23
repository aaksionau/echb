from .base import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS += ('debug_toolbar',)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

USE_TZ = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'echb_test',
        'USER': 'postgres',
        'PASSWORD': config('DB_PASSWORD_TEST'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}