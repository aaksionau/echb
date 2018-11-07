import os
from .base import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS = []
INTERNAL_IPS = ['127.0.0.1', ]
INSTALLED_APPS += ('debug_toolbar',)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME_STAGE'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '5432',
    }
}
STATIC_URL = '/static/'
STATIC_ROOT = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media/')

"""
def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK" : show_toolbar,
}
"""
