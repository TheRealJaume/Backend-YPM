from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create a router and register our ViewSets with it.
from company.company.views import CompanyViewset
from company.department.views import CompanyDepartmentViewset, DepartmentViewset
from company.workers.views import WorkerViewset

router = DefaultRouter()
router.register(r'^company', CompanyViewset, basename='company')
router.register(r'^company-department', CompanyDepartmentViewset, basename='company_department')
router.register(r'^department', DepartmentViewset, basename='department')
router.register(r'^worker', WorkerViewset, basename='worker')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
