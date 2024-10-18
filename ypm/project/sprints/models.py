from django.db import models
# from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel
#
#
# # PROJECT TASK
# class ProjectTask(UUIDModel, SoftDeletableModel, TimeStampedModel):
#     """ Model representing a Task of a Project """
#     name = models.CharField(max_length=240, null=False, blank=False)
#     description = models.TextField(blank=True, null=True)
#     time = models.IntegerField(null=True, blank=True)  # In minutes
#     sprint = models.ForeignKey("projects.ProjectSprint", null=True, blank=True,
#                                on_delete=models.CASCADE, related_name='sprints')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         db_table = 'projects_project_task'