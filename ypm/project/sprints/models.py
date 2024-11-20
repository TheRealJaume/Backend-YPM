from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


# PROJECT SPRINT
class ProjectSprint(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a Sprint of a Project """
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE, related_name='project',
                                db_column="project")
    name = models.CharField(max_length=240, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    time = models.IntegerField(null=False, blank=False, default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'projects_project_sprint'
