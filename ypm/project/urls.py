from django.urls import path, include
from rest_framework.routers import DefaultRouter

from project.departments.views import ProjectDepartmentViewset
from project.projects.views import ProjectViewset
from project.tasks.views import TaskViewset
from project.technologies.views import ProjectTechnologyViewset
from project.workers.views import ProjectWorkerViewset
# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register('project',  ProjectViewset, basename='project')
router.register('project-technology',  ProjectTechnologyViewset, basename='project-technology')
router.register('project-worker',  ProjectWorkerViewset, basename='project-worker')
router.register('project-department',  ProjectDepartmentViewset, basename='project-department')
router.register('project-task',  TaskViewset, basename='project-task')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
