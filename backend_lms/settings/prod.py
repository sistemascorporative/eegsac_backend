from .base import *

DEBUG = False

# Seguridad HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# Railway suele necesitar esto:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ALLOWED_HOSTS = [
  'eegsac.up.railway.app',
  'eegsac.com',
  'www.eegsac.com'
]

DATABASES = {
    'default': dj_database_url.config(
      default=os.getenv('DATABASE_URL')
    ) # produccion
}

CSRF_TRUSTED_ORIGINS = ['https://eegsac.up.railway.app']

CORS_ALLOWED_ORIGINS = [
    'https://eegsac.com',
    'https://www.eegsac.com',
    'https://educacion.eegsac.com',
    'https://www.educacion.eegsac.com',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DOMAIN = 'https://educacion.eegsac.com'
