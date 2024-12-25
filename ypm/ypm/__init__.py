from __future__ import absolute_import, unicode_literals
from ypm.celery import app as celery_app
from django.core.files.storage import get_storage_class

__all__ = ('celery_app',)

# Forzar inicialización de default_storage basado en la configuración actual
StorageClass = get_storage_class()
default_storage = StorageClass()
