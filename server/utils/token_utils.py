import secrets
from django.utils import timezone
from datetime import timedelta
from userApp.models import EmailVerificationToken, PasswordResetToken


def generate_verification_token(user):
    token = secrets.token_urlsafe(32)
    expires_at = timezone.now() + timedelta(hours=24)
    
    EmailVerificationToken.objects.create(
        user=user,
        token=token,
        expires_at=expires_at
    )
    
    return token

def generate_password_reset_token(user):
    token = secrets.token_urlsafe(32)
    expires_at = timezone.now() + timedelta(hours=24)
    
    PasswordResetToken.objects.create(
        user=user,
        token=token,
        expires_at=expires_at
    )
    
    return token