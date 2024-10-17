from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel
from project.projects.models import Project


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
