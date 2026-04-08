from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile, UserWallet, AdminProfile


@receiver(post_save, sender=User)
def handle_new_user(sender, instance, created, **kwargs):
    if created:
        # Every new user gets a profile and wallet
        UserProfile.objects.create(user=instance)
        UserWallet.objects.create(user=instance)

        # First user ever gets super admin
        if User.objects.count() == 1:
            AdminProfile.objects.create(
                user=instance,
                admin_username=instance.email,
                is_super_admin=True
            )
            instance.is_staff = True
            instance.is_superuser = True
            instance.save()