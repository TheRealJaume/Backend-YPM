from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


# PROJECT REQUIREMENT
class ProjectRequirement(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a Project Requirement """
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='requirements',
                                db_column="project")
    requirement = models.TextField(null=False, blank=False)

    def __str__(self):
        return self.requirement

    class Meta:
        db_table = 'projects_project_requirements'
