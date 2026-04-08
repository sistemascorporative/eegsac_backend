from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    #'default': dj_database_url.config(default=os.getenv('DATABASE_URL') # produccion)
    #'default': dj_database_url.parse(os.getenv('DATABASE_PUBLIC_URL'))
}


CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    'http://*'
]

CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DOMAIN = 'localhost:5173'