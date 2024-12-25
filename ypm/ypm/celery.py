from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from django.utils.module_loading import import_string

# Detectar el entorno (por defecto 'local')
env = os.getenv("DJANGO_ENV", "local")  # Cambia automáticamente según la variable DJANGO_ENV

# Configurar DJANGO_SETTINGS_MODULE según el entorno
if env == "production":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ypm.settings.production")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ypm.settings.local")

# Crear la aplicación Celery
app = Celery("ypm")

# Leer la configuración desde Django settings y usar el prefijo 'CELERY_'
app.config_from_object("django.conf:settings", namespace="CELERY")

# Descubrir automáticamente las tareas de los módulos instalados
app.autodiscover_tasks()

# Inicializar el almacenamiento predeterminado
StorageClass = import_string(settings.DEFAULT_FILE_STORAGE)
default_storage = StorageClass()

# Log para confirmar el entorno y configuración en uso
@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
