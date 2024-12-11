from django.urls import path, include
from rest_framework.routers import DefaultRouter

from payments.coins.views import UserCoinViewSet
from payments.payments.views import UserPaymentsViewSet
from payments.views import StripeViewSet

router = DefaultRouter()

router.register('stripe', StripeViewSet, basename='stripe')
router.register('coins', UserCoinViewSet, basename='coins')
router.register('user_payment', UserPaymentsViewSet, basename='user_payments')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]