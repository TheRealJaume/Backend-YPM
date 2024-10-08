from django.contrib import admin
from django.urls import path, include
from users.views import google_login, refresh_token

urlpatterns = [
    path('admin/', admin.site.urls),
    # auth and token
    path('accounts/', include('allauth.urls')),
    path('auth/google/', google_login, name='google_login'),
    path('auth/token/refresh/', refresh_token, name='refresh_token'),
]
