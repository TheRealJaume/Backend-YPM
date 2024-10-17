from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel

from project.projects.models import Project


# PROJECT WORKER


class ProjectWorker(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing the association between Worker and Project """
    worker = models.ForeignKey('company.Worker', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=240, blank=True, null=True)

    class Meta:
        unique_together = ('worker', 'project')

    def __str__(self):
        return f"{self.worker} - {self.project}"

    class Meta:
        db_table = 'projects_project_workers'




