from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserViewset
# Create a router and register our ViewSets with it.

router = DefaultRouter()
router.register(r'^user', UserViewset, basename='company')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
