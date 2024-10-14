from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create a router and register our ViewSets with it.
from project.views import ProjectViewset


router = DefaultRouter()
router.register(r'^project',  ProjectViewset, basename='project')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
