from .base import *
from decouple import config

DEBUG = False

INSTALLED_APPS += ('django_summernote','newsevents','churches', 'articles', 'galleries', 'social_django', 'pages',)

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

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True