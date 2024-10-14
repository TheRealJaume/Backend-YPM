from django.contrib import admin

# Register your models here.
from company.company.models import Company
from company.workers.models import Worker
from company.department.models import Department

admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Worker)
