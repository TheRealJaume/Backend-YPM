from django.urls import path, include
from rest_framework.routers import DefaultRouter


# Create a router and register our ViewSets with it.
from tasks.views import TaskViewset

router = DefaultRouter()
router.register('', TaskViewset, basename='project-task')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
