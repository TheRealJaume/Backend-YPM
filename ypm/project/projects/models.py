from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


# PROJECT
class Project(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a Project of a company """
    name = models.CharField(max_length=240, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='projects')
    init_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'projects_project'


# PROJECT REQUIREMENT
class ProjectRequirement(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a Project Requirement """
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='requirements', db_column="project")
    requirement = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.requirement

    class Meta:
        db_table = 'projects_project_requirements'
