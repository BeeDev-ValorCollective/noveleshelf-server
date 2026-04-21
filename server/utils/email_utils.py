from django.core.mail import send_mail
from django.conf import settings
from .token_utils import generate_verification_token, generate_password_reset_token


def send_verification_email(user):
    token = generate_verification_token(user)
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    
    send_mail(
        subject='Verify your NovelShelf account',
        message=f'''Welcome to NovelShelf!

Please verify your email address by clicking the link below:

{verification_url}

This link expires in 24 hours.

This email was sent to {user.email}. If you did not create an account please ignore this email.

The NovelShelf Team''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

def send_password_reset_email(user):
    token = generate_password_reset_token(user)
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    
    send_mail(
        subject='Reset your NovelShelf password',
        message=f'''Hi there,

We received a request to reset the password for your NovelShelf account associated with {user.email}.

Click the link below to reset your password:

{reset_url}

This link expires in 24 hours.

If you did not request a password reset please ignore this email. Your password will not be changed.

The NovelShelf Team''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )