from django.contrib import admin

from project.departments.models import ProjectDepartment
from project.projects.models import Project
from project.technologies.models import ProjectTechnology
from project.workers.models import ProjectWorker

admin.site.register(Project)
admin.site.register(ProjectTechnology)
admin.site.register(ProjectWorker)
admin.site.register(ProjectDepartment)
