from datetime import timedelta

from django.db.models import Sum

from project.sprints.models import ProjectSprint
from project.task.models import ProjectTask


class SprintManagerV0:

    def __init__(self, project):
        self.project = project
        self.sprints = ProjectSprint.objects.filter(project=self.project)

    def get_sprint_end_date(self, sprint, start_date):
        sprint_tasks = ProjectTask.objects.filter(sprint=sprint)
        tasks_time = sprint_tasks.aggregate(total_time=Sum('time'))['total_time']
        sprint_end_date = start_date + timedelta(hours=tasks_time)
        return tasks_time, sprint_end_date
