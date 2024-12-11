from django.db import models
from model_utils.models import SoftDeletableModel, UUIDModel


class UserCoin(UUIDModel, SoftDeletableModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    coins = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = 'payments_user_coins'