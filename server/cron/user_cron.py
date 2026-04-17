from django.utils import timezone
from userApp.models import User


def deactivate_unverified_users():
    expired_users = User.objects.filter(
        is_verified=False,
        is_active=True,
        verification_grace_ends__lt=timezone.now()
    )
    
    count = expired_users.count()
    expired_users.update(is_active=False)
    
    print(f'Deactivated {count} unverified users past grace period')