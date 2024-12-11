from django.urls import path, include
from rest_framework.routers import DefaultRouter
from technologies.views import TechnologyViewset

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register('technology',  TechnologyViewset, basename='technology')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
