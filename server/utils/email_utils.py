from django.core.mail import EmailMessage
from django.conf import settings
from utils.token_utils import generate_verification_token, generate_password_reset_token
import logging

logger = logging.getLogger(__name__)


def _get_bcc():
    """Returns BCC list if BCC_EMAIL is set in settings."""
    bcc_email = getattr(settings, 'BCC_EMAIL', None)
    return [bcc_email] if bcc_email else []


# ─── Direct user emails (always send, no preferences) ─────────────────────────

def send_verification_email(user):
    try:
        token = generate_verification_token(user)
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"

        email = EmailMessage(
            subject='Verify your Novel eShelf account',
            body=f'''Welcome to Novel eShelf!

Please verify your email address by clicking the link below:

{verification_url}

This link expires in 24 hours.

This email was sent to {user.email}. If you did not create an account please ignore this email.

The Novel eShelf Team''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
            bcc=_get_bcc(),
        )
        email.send(fail_silently=False)
        logger.info(f'Verification email sent to {user.email}')
    except Exception as e:
        logger.error(f'Failed to send verification email to {user.email}: {e}')


def send_password_reset_email(user):
    try:
        token = generate_password_reset_token(user)
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"

        email = EmailMessage(
            subject='Reset your Novel eShelf password',
            body=f'''Hi there,

We received a request to reset the password for your Novel eShelf account associated with {user.email}.

Click the link below to reset your password:

{reset_url}

This link expires in 24 hours.

If you did not request a password reset please ignore this email. Your password will not be changed.

The Novel eShelf Team''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
            bcc=_get_bcc(),
        )
        email.send(fail_silently=False)
        logger.info(f'Password reset email sent to {user.email}')
    except Exception as e:
        logger.error(f'Failed to send password reset email to {user.email}: {e}')


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

Please note that your reader account remains active. You can still log in and enjoy reading on Novel eShelf at:
{settings.FRONTEND_URL}/login

If you wish to reactivate your author profile in the future please submit a rejoin request through your dashboard.

Thank you for being part of Novel eShelf.

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

The Novel eShelf Team'''

    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
            bcc=_get_bcc(),
        )
        email.send(fail_silently=False)
        logger.info(f'Author approved email ({request_type}) sent to {user.email}')
    except Exception as e:
        logger.error(f'Failed to send author approved email to {user.email}: {e}')


def send_author_deactivated_email(user):
    try:
        email = EmailMessage(
            subject='Novel eShelf — Author profile deactivated',
            body=f'''Hi there,

Your paid author profile on Novel eShelf has been deactivated as requested.

Your books are no longer visible to new readers. Readers who have already unlocked your chapters will retain access to those chapters.

Please note that your reader account remains active. You can still log in and enjoy reading on Novel eShelf at:
{settings.FRONTEND_URL}/login

If you wish to reactivate your author profile in the future please submit a rejoin request through your dashboard.

The Novel eShelf Team''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
            bcc=_get_bcc(),
        )
        email.send(fail_silently=False)
        logger.info(f'Author deactivated email sent to {user.email}')
    except Exception as e:
        logger.error(f'Failed to send author deactivated email to {user.email}: {e}')


def send_author_reactivated_email(user):
    try:
        email = EmailMessage(
            subject='Novel eShelf — Author profile reactivated',
            body=f'''Welcome back!

Your author profile on Novel eShelf has been reactivated.

You can now log in and access your author dashboard at:
{settings.FRONTEND_URL}/login

Please note that your books visibility will need to be manually updated by the admin team. Please contact us through the dashboard to discuss which books should be made available again.

The Novel eShelf Team''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
            bcc=_get_bcc(),
        )
        email.send(fail_silently=False)
        logger.info(f'Author reactivated email sent to {user.email}')
    except Exception as e:
        logger.error(f'Failed to send author reactivated email to {user.email}: {e}')


# ─── Central notification sender ──────────────────────────────────────────────

def send_notification(notification_code, user=None, triggered_by=None, context=None):
    try:
        from notificationApp.models import NotificationType, NotificationPreference, SystemNotificationEmail, Notification
        from userApp.models import AdminProfile, ModeratorProfile

        notification_type = NotificationType.objects.get(
            code=notification_code,
            is_active=True
        )
    except Exception as e:
        logger.error(f'Notification type not found: {notification_code} — {e}')
        return

    context = context or {}
    email_subject, email_message = _build_email_content(notification_code, user, triggered_by, context)

    if not email_subject or not email_message:
        logger.warning(f'No email content for notification type: {notification_code}')
        return

    recipients = set()

    if notification_type.sends_to_user and user:
        recipients.add(user.email)
        Notification.objects.create(
            user=user,
            notification_type=notification_type,
            message=_build_bell_message(notification_code, user, triggered_by, context)
        )

    if notification_type.sends_to_admins:
        from userApp.models import User
        admin_users = User.objects.filter(
            admin_profile__isnull=False
        ) | User.objects.filter(
            moderator_profile__isnull=False
        )

        for admin_user in admin_users:
            preference = NotificationPreference.objects.filter(
                user=admin_user,
                notification_type=notification_type
            ).first()

            is_enabled = preference.is_enabled if preference else True

            if is_enabled:
                recipients.add(admin_user.email)
                Notification.objects.create(
                    user=admin_user,
                    notification_type=notification_type,
                    message=_build_bell_message(notification_code, user, triggered_by, context)
                )

        system_emails = SystemNotificationEmail.objects.filter(
            is_active=True,
            notification_types=notification_type
        )
        for system_email in system_emails:
            recipients.add(system_email.email)

    if recipients:
        try:
            email = EmailMessage(
                subject=email_subject,
                body=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=list(recipients),
                bcc=_get_bcc(),
            )
            email.send(fail_silently=False)
            logger.info(f'Notification email ({notification_code}) sent to {recipients}')
        except Exception as e:
            logger.error(f'Email send error for {notification_code}: {e}')


def _build_email_content(notification_code, user, triggered_by, context):
    user_email = user.email if user else 'Unknown'
    triggered_by_email = triggered_by.email if triggered_by else 'System'

    templates = {
        'new_user_registered': (
            'Novel eShelf — New User Registered',
            f'A new user has registered on Novel eShelf.\n\nEmail: {user_email}\n\nLog in to the admin dashboard to view details.'
        ),
        'free_author_upgrade': (
            'Novel eShelf — New Free Author',
            f'{user_email} has upgraded to a free author on Novel eShelf.\n\nLog in to the admin dashboard to view details.'
        ),
        'new_author_request': (
            'Novel eShelf — New Author Request',
            f'{user_email} has submitted a new author request.\n\nRequest type: {context.get("request_type", "Unknown")}\n\nLog in to the admin dashboard to review.'
        ),
        'author_request_approved': (
            'Novel eShelf — Author Request Approved',
            f'Your author request has been approved.\n\nLog in to your dashboard to get started:\n{settings.FRONTEND_URL}/login'
        ),
        'author_request_status_change': (
            'Novel eShelf — Author Request Update',
            f'Your author request status has been updated to: {context.get("status", "Unknown")}\n\n{context.get("reader_notes", "")}\n\nLog in to view details:\n{settings.FRONTEND_URL}/login'
        ),
        'book_submitted_for_approval': (
            'Novel eShelf — Book Submitted for Approval',
            f'{user_email} has submitted a book for approval.\n\nBook: {context.get("book_title", "Unknown")}\n\nLog in to the admin dashboard to review.'
        ),
        'book_status_change': (
            'Novel eShelf — Book Status Update',
            f'Your book "{context.get("book_title", "Unknown")}" status has been updated to: {context.get("status", "Unknown")}\n\n{context.get("reader_notes", "")}\n\nLog in to view details:\n{settings.FRONTEND_URL}/login'
        ),
        'flagged_content': (
            'Novel eShelf — Flagged Content',
            f'New flagged content requires review.\n\nType: {context.get("content_type", "Unknown")}\n\nLog in to the admin dashboard to review.'
        ),
        'author_deactivated': (
            'Novel eShelf — Author Deactivated',
            f'Author profile deactivated.\n\nAuthor: {user_email}\nDeactivated by: {triggered_by_email}\n\nLog in to the admin dashboard for details.'
        ),
        'author_reactivated': (
            'Novel eShelf — Author Reactivated',
            f'Author profile reactivated.\n\nAuthor: {user_email}\nReactivated by: {triggered_by_email}\n\nLog in to the admin dashboard for details.'
        ),
    }

    return templates.get(notification_code, (None, None))


def _build_bell_message(notification_code, user, triggered_by, context):
    user_email = user.email if user else 'Unknown'

    messages = {
        'new_user_registered': f'New user registered: {user_email}',
        'free_author_upgrade': f'{user_email} upgraded to free author',
        'new_author_request': f'New author request from {user_email}',
        'author_request_approved': 'Your author request has been approved',
        'author_request_status_change': f'Your author request status changed to {context.get("status", "Unknown")}',
        'book_submitted_for_approval': f'New book submitted for approval: {context.get("book_title", "Unknown")}',
        'book_status_change': f'Your book "{context.get("book_title", "Unknown")}" status changed to {context.get("status", "Unknown")}',
        'flagged_content': f'New flagged {context.get("content_type", "content")} requires review',
        'author_deactivated': f'Author {user_email} has been deactivated',
        'author_reactivated': f'Author {user_email} has been reactivated',
    }

    return messages.get(notification_code, 'You have a new notification')