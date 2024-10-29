from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


# PROJECT TASK
class ProjectJira(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a Jira Project """
    key = models.CharField(max_length=240, null=False, blank=False)
    name = models.CharField(max_length=240, null=False, blank=False)
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE, db_column="project")

    def __str__(self):
        return self.key

    class Meta:
        db_table = 'projects_project_jira'
