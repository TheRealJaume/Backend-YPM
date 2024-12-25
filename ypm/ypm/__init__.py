from __future__ import absolute_import, unicode_literals
from ypm.celery import app as celery_app
from django.conf import settings
from django.utils.module_loading import import_string

__all__ = ('celery_app',)

# Inicializar el almacenamiento predeterminado
StorageClass = import_string(settings.DEFAULT_FILE_STORAGE)
default_storage = StorageClass()