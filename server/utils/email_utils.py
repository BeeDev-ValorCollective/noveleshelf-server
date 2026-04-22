from django.core.mail import send_mail
from django.conf import settings
from .token_utils import generate_verification_token, generate_password_reset_token


def send_verification_email(user):
    token = generate_verification_token(user)
    verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"
    
    send_mail(
        subject='Verify your Novel eShelf account',
        message=f'''Welcome to Novel eShelf!

Please verify your email address by clicking the link below:

{verification_url}

This link expires in 24 hours.

This email was sent to {user.email}. If you did not create an account please ignore this email.

The Novel eShelf Team''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

def send_password_reset_email(user):
    token = generate_password_reset_token(user)
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"
    
    send_mail(
        subject='Reset your Novel eShelf password',
        message=f'''Hi there,

We received a request to reset the password for your Novel eShelf account associated with {user.email}.

Click the link below to reset your password:

{reset_url}

This link expires in 24 hours.

If you did not request a password reset please ignore this email. Your password will not be changed.

The Novel eShelf Team''',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

def send_author_approved_email(user, request_type):
    if request_type == 'new_author':
        subject = 'Welcome to Novel eShelf — You are now a paid author!'
        message = f'''Congratulations!

Your request to become a paid author on Novel eShelf has been approved.

You can now log in and access your author dashboard at:
{settings.FRONTEND_URL}/login

Please make sure to:
- Set up your author username and pen name
- Review your author profile
- Start uploading your books

If you have any questions please contact us through the admin dashboard.

The Novel eShelf Team'''

    elif request_type == 'leave_platform':
        subject = 'Novel eShelf — Your departure has been processed'
        message = f'''Hi there,

Your request to leave the Novel eShelf platform has been processed.

Your author profile has been deactivated and your books are no longer visible to new readers. Readers who have already unlocked your chapters will retain access.

If you ever wish to return please submit a rejoin request through your dashboard.

The Novel eShelf Team'''

    elif request_type == 'rejoin_platform':
        subject = 'Welcome back to Novel eShelf!'
        message = f'''Welcome back!

Your request to rejoin Novel eShelf as a paid author has been approved.

You can now log in and access your author dashboard at:
{settings.FRONTEND_URL}/login

Please contact admin to discuss your contract and which books will be made available again.

The Novel eShelf Team'''

    else:
        subject = 'Novel eShelf — Your request has been approved'
        message = f'''Hi there,

Your request has been approved by the Novel eShelf team.

Please log in to your dashboard for more details:
{settings.FRONTEND_URL}/login

If you have any questions please contact us through the admin dashboard.

The NovelShelf Team'''

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )