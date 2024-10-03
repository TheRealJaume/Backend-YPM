from django.contrib import admin
from django.urls import path, include
from users.views import google_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('auth/google/', google_login, name='google_login'),

]
