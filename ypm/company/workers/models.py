from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


class Worker(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a worker """
    first_name = models.CharField(max_length=240, null=False, blank=False)
    last_name = models.CharField(max_length=240, null=False, blank=False)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='workers')

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'companies_worker'
