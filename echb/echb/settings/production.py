from .base import *
from decouple import config

DEBUG = False

ALLOWED_HOSTS = ['ecb.kh.ua','www.ecb.kh.ua']

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
    os.path.join(BASE_DIR, "static")
]
STATIC_ROOT = '/home/paloni/webapps/echb_static/'

MEDIA_ROOT = os.path.join(BASE_DIR, '/home/paloni/webapps/echb_static/media/')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True

EMAIL_HOST = config('SMTP_SERVER')
EMAIL_PORT = config('SMTP_PORT')
EMAIL_HOST_USER = config('MAIL_USER')
EMAIL_HOST_PASSWORD = config('MAIL_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

FILE_UPLOAD_MAX_MEMORY_SIZE = 6021440
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o644
FILE_UPLOAD_PERMISSIONS = 0o644