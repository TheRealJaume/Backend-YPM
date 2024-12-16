from .base import *

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
    "https://ai-ypm.onrender.com",
    "https://frontend-ypm.vercel.app",
    "https://d236c2bpjduxda.cloudfront.net",
    "https://yourpm.pro",
    "127.0.0.1",
    "localhost"
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

# Archivos estáticos y media para producción
STATIC_ROOT = "/var/www/myproject/static/"
MEDIA_ROOT = "/var/www/myproject/media/"

# Configuración de seguridad
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
