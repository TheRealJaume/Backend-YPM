from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


class Department(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a company """
    name = models.CharField(max_length=240, null=False, blank=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'departments_department'


class CompanyDepartment(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a company """
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='companies')
    department = models.ForeignKey('company.Department', on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'departments_company_department'
