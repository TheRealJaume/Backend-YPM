from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create a router and register our ViewSets with it.
from project.views import ProjectViewset, ProjectTechnologyViewset


router = DefaultRouter()
router.register(r'^project',  ProjectViewset, basename='project')
router.register(r'^project-technology',  ProjectTechnologyViewset, basename='project-technology')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
