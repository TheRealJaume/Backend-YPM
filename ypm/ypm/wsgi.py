"""
WSGI config for ypm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application

# Determinar el entorno automáticamente (puedes usar otra lógica si lo prefieres)
env = os.getenv('DJANGO_ENV', 'local')  # Por defecto usa 'local'
print(f"Running in environment: {env}")
if env == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ypm.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ypm.settings.local')

application = get_wsgi_application()