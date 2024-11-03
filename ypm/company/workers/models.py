from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


class Worker(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a worker """
    first_name = models.CharField(max_length=240, null=False, blank=False)
    last_name = models.CharField(max_length=240, null=False, blank=False)
    time = models.IntegerField(null=False, blank=False)
    level = models.CharField(max_length=240, null=False, blank=False)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='workers')

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = 'companies_worker'


class WorkerTechnology(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a worker technology """
    worker = models.ForeignKey('company.Worker', on_delete=models.CASCADE, db_column="worker")
    technology = models.ForeignKey('technologies.Technology', on_delete=models.CASCADE, db_column="technology")

    def __str__(self):
        return self.worker.first_name + " " + self.worker.last_name + " " + self.technology.name

    class Meta:
        db_table = 'companies_worker_technology'
