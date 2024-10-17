from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel

from project.projects.models import Project


# PROJECT DEPARTMENT
class ProjectDepartment(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing the association between Project and Department """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, db_column="project")
    department = models.ForeignKey('company.Department', on_delete=models.CASCADE, db_column="departments")

    class Meta:
        unique_together = ('project', 'department')

    def __str__(self):
        return f"{self.project} - {self.department}"

    class Meta:
        db_table = 'projects_project_department'
