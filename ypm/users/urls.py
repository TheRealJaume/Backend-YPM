from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.jira.views import JiraUserViewset
from users.views import UserViewset
# Create a router and register our ViewSets with it.

router = DefaultRouter()
router.register('user', UserViewset, basename='user')
router.register('jira', JiraUserViewset, basename='jira')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
