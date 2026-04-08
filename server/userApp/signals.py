from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile, UserWallet, AdminProfile


@receiver(post_save, sender=User)
def handle_new_user(sender, instance, created, **kwargs):
    if created:
        instance.default_login_role = 'reader'
        instance.save()
        UserProfile.objects.create(user=instance)
        UserWallet.objects.create(user=instance)

        if User.objects.count() == 1:
            AdminProfile.objects.create(
                user=instance,
                admin_username=instance.email,
                is_super_admin=True
            )
            instance.is_staff = True
            instance.is_superuser = True
            instance.save()