from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


class Company(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a company """
    name = models.CharField(max_length=240, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='companies', db_column="owner")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'companies_company'
