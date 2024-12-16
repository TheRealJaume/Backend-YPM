from .base import *

# Entorno de desarrollo
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# CORS para desarrollo
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:5173",
]

# Base de datos SQLite para desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Archivos estáticos en local
STATICFILES_DIRS = [BASE_DIR / 'staticfiles']
