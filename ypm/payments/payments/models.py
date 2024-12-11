from django.db import models
from model_utils.models import SoftDeletableModel, TimeStampedModel, UUIDModel


class UserPayments(UUIDModel, SoftDeletableModel, TimeStampedModel):
    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_FAILED, 'Failed'),
    ]

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, db_column='user')
    amount = models.IntegerField(default=0, null=False, blank=False)
    coins = models.IntegerField(default=0, null=False, blank=False)
    transaction_id = models.CharField(max_length=240, null=False, blank=False)
    status = models.CharField(choices=STATUS_CHOICES, default=STATUS_PENDING, max_length=20)

    class Meta:
        db_table = 'payments_user_payments'
