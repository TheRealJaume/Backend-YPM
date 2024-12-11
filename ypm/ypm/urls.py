from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from users.views import google_login, google_logout, refresh_token, onboarding
from project.urls import urlpatterns as project_urls
from company.urls import urlpatterns as company_urls
from payments.urls import urlpatterns as payment_urls
from users.urls import urlpatterns as user_urls
from technologies.urls import urlpatterns as technology_urls
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # auth and token
    path('accounts/', include('allauth.urls')),
    path('login/google', google_login, name='google_login'),
    path('logout', google_logout, name='google_logout'),
    path('token/refresh/', refresh_token, name='refresh_token'),
    path('onboarding/', onboarding, name='onboarding'),
    # company
    path('', include(company_urls), name='company'),
    # project
    path('', include(project_urls), name='project'),
    # user
    path('', include(user_urls), name='user'),
    # technology
    path('', include(technology_urls), name='technology'),
    # payments
    path('', include(payment_urls), name='payment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
