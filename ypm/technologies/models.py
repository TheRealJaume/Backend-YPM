from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


class Technology(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a Technologies """
    name = models.CharField(max_length=240, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    group = models.CharField(max_length=240, null=False, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'technologies_technology'
