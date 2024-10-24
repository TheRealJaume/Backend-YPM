from django.contrib import admin

from project.departments.models import ProjectDepartment
from project.projects.models import Project
from project.sprints.models import ProjectSprint
from project.tasks.models import ProjectTask
from project.technologies.models import ProjectTechnology
from project.workers.models import ProjectWorker

admin.site.register(Project)
admin.site.register(ProjectTechnology)
admin.site.register(ProjectWorker)
admin.site.register(ProjectDepartment)
admin.site.register(ProjectSprint)
admin.site.register(ProjectTask)
