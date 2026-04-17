from django.core.mail import send_mail
from django.conf import settings
from .token_utils import generate_verification_token


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