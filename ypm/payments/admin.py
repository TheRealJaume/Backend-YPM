from django.contrib import admin

# Register your models here.
from payments.coins.models import UserCoin
from payments.payments.models import UserPayments

admin.site.register(UserCoin)
admin.site.register(UserPayments)