from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


# PROJECT TASK
class ProjectTask(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing a Task of a Project """
    name = models.CharField(max_length=240, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    time = models.IntegerField(null=True, blank=True)  # In minutes
    sprint = models.ForeignKey("project.ProjectSprint", null=True, blank=True,
                               on_delete=models.CASCADE, related_name='sprints')
    project = models.ForeignKey("project.Project", on_delete=models.CASCADE, db_column="project")
    phase = models.ForeignKey("project.ProjectPhase", on_delete=models.CASCADE, db_column="phase")
    department = models.ForeignKey("project.ProjectDepartment", on_delete=models.CASCADE, db_column="department")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'projects_project_task'


# TASK WORKER
class ProjectTaskWorker(UUIDModel, SoftDeletableModel, TimeStampedModel):
    """ Model representing the worker(s) assigned to a project task"""
    worker = models.ForeignKey("company.Worker", on_delete=models.CASCADE, db_column="worker")
    task = models.ForeignKey("project.ProjectTask", on_delete=models.CASCADE, db_column="task")

    def __str__(self):
        return self.worker.first_name + " " + self.task.name

    class Meta:
        db_table = 'projects_project_task_workers'
