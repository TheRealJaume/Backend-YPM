from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
# Entorno de producción

DEBUG = False

ALLOWED_HOSTS = [
    "ec2-3-248-226-39.eu-west-1.compute.amazonaws.com",
    "api.yourpm.pro",
    "yourpm.pro",
    "34.242.245.215"
]

# CORS para producción
CORS_ALLOWED_ORIGINS = [
    "https://d236c2bpjduxda.cloudfront.net",
    "https://yourpm.pro",
    "127.0.0.1",
    "localhost"
]

# Opcional: permite credenciales (si usas autenticación con cookies)
CORS_ALLOW_CREDENTIALS = True

# Opcional: permitir todos los métodos HTTP
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
]

CORS_ALLOW_HEADERS = [
    "Authorization",
    "Content-Type",
    "Accept",
    "Origin",
    "X-Requested-With",
]

# Base de datos PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRESQL_HOST'),
        'PORT': os.getenv('POSTGRESQL_PORT'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Sentry Configuration
sentry_sdk.init(
    dsn="https://4801ecf75f8f88b74622f1ee3a73a9ae@o4508494681866240.ingest.de.sentry.io/4508494684422224",
    traces_sample_rate=1.0,
    integrations=[DjangoIntegration()],
    _experiments={
        "continuous_profiling_auto_start": True,
    },
)

# Archivos estáticos y media para producción
STATIC_ROOT = "/ypm/staticfiles/"
MEDIA_ROOT = "/var/www/Backend-YPM/ypm/media/"

# Configuración de seguridad
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
