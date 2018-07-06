from .base import *

DEBUG = False

INSTALLED_APPS += []

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'echb_stage',
        'USER': 'echb',
        'PASSWORD': 'kyICJphjf8thuYex39Ch',
        'HOST': 'web528.webfaction.com',
        'PORT': '5432',
    }
}