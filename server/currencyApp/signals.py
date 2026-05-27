from django.db.models.signals import post_save
from django.dispatch import receiver
from userApp.models import User
from .models import DailyLoginReward


@receiver(post_save, sender=User)
def handle_new_user_currency(sender, instance, created, **kwargs):
    if created:
        DailyLoginReward.objects.create(user=instance)