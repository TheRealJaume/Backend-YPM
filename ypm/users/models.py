import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    onboarding = models.BooleanField(default=False)
    language = models.CharField(null=True, blank=True, choices=getattr(settings, 'LANGUAGES', []), default="es")

    def __str__(self):
        return self.email

    class Meta:
        db_table = "users_user"