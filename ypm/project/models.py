from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel

from company.workers.models import Worker


# PROJECT
class Project(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a Project of a company """
    name = models.CharField(max_length=240, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'projects_project'


# PROJECT WORKER
class ProjectWorker(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing the association between Worker and Project """
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=240, blank=True, null=True)

    class Meta:
        unique_together = ('worker', 'project')

    def __str__(self):
        return f"{self.worker} - {self.project}"

    class Meta:
        db_table = 'projects_project_workers'


# PROJECT TECHNOLOGY
class ProjectTechnology(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing the association between Project and Technology """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column="project")
    technology = models.ForeignKey('technologies.Technology', on_delete=models.CASCADE, db_column="technology")

    class Meta:
        unique_together = ('project', 'technology')

    def __str__(self):
        return f"{self.project} - {self.technology}"

    class Meta:
        db_table = 'projects_project_technologies'
