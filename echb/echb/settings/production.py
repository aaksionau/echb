from .base import *
from decouple import config

DEBUG = False



ALLOWED_HOSTS = ['paloni.webfactional.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '5432',
    }
}

STATICFILES_DIRS = [
]
STATIC_ROOT = '/home/paloni/webapps/echb_static/'