from django.db.models.signals import post_save
from django.dispatch import receiver

from payments.coins.models import UserCoin
from users.models import User


@receiver(post_save, sender=User)
def create_user_coin(sender, instance, created, **kwargs):
    if created:
        print("ENTRO")
        print("instance")
        user_coins = UserCoin(user=instance, coins=0)
        user_coins.save()
    return True
