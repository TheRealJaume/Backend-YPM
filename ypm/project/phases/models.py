from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


# PROJECT PHASE
class ProjectPhase(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a Project of a company """
    name = models.CharField(max_length=240, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, db_column='project')
    #TODO: Incluir project_type

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'projects_project_phase'
