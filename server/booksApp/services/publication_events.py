
import logging

from django.contrib.auth import get_user_model
from django.db import transaction

from booksApp.models import UserBook
from booksApp.services.expo_push import (
    send_expo_push_notifications,
)

from notificationApp.models import (
    Notification,
    NotificationType,
    NotificationPreference,
    NotificationPermission,
)


User = get_user_model()
logger = logging.getLogger(__name__)


def get_book_publication_recipients(book):
    """
    Users following the book's author,
    excluding the author themselves.
    """

    if book.author_profile:
        profile = book.author_profile

    elif book.free_author_profile:
        profile = book.free_author_profile

    else:
        return User.objects.none()

    user_ids = profile.followers.values_list(
        'user_id',
        flat=True
    )

    return (
        User.objects
        .filter(id__in=user_ids)
        .exclude(id=profile.user_id)
        .distinct()
    )


def get_chapter_publication_recipients(chapter):
    """
    Users who have this book on their shelf.
    """

    user_ids = (
        UserBook.objects
        .filter(book=chapter.book)
        .values_list('user_id', flat=True)
    )

    return (
        User.objects
        .filter(id__in=user_ids)
        .distinct()
    )


def get_publication_notification_type(code):
    """
    Find or create the notification type used
    by publication events.
    """

    definitions = {
        'book_published': {
            'label': 'New Book Published',
            'description': (
                'An author you follow published a book.'
            ),
        },
        'chapter_published': {
            'label': 'New Chapter Published',
            'description': (
                'A book on your shelf has a new chapter.'
            ),
        },
    }

    definition = definitions[code]

    notification_type, created = (
        NotificationType.objects.get_or_create(
            code=code,
            defaults={
                **definition,
                'recipient_type': 'user',
                'sends_to_user': True,
                'sends_to_admins': False,
                'is_active': True,
            },
        )
    )

    return notification_type


def get_push_enabled_user_ids(
    user_ids,
    notification_type
):
    """
    Determine which recipients allow push alerts.

    No preference means enabled by default.
    Explicitly disabled preferences suppress push.
    Explicitly denied permissions suppress push.
    """

    if not notification_type.is_active:
        return []

    if not notification_type.sends_to_user:
        return []

    disabled_preferences = set(
        NotificationPreference.objects.filter(
            user_id__in=user_ids,
            notification_type=notification_type,
            is_enabled=False,
        ).values_list('user_id', flat=True)
    )

    denied_permissions = set(
        NotificationPermission.objects.filter(
            user_id__in=user_ids,
            notification_type=notification_type,
            is_allowed=False,
        ).values_list('user_id', flat=True)
    )

    return [
        user_id
        for user_id in user_ids
        if user_id not in disabled_preferences
        and user_id not in denied_permissions
    ]


def create_publication_notifications(
    user_ids,
    notification_type,
    title,
    message,
    book,
    chapter=None,
):
    """
    Create in-app notifications independently
    of push notification preferences.

    Returns IDs of users whose notifications
    were newly created.
    """

    created_user_ids = []

    for user_id in user_ids:
        lookup = {
            'user_id': user_id,
            'notification_type': notification_type,
            'book': book,
            'chapter': chapter,
        }

        # Avoid matching an unrelated notification
        # when no chapter is associated with the event.
        notification, created = (
            Notification.objects.get_or_create(
                **lookup,
                defaults={
                    'title': title,
                    'message': message,
                    'is_read': False,
                },
            )
        )

        if created:
            created_user_ids.append(user_id)

    return created_user_ids


def publish_notification_event(
    recipients,
    type_code,
    title,
    message,
    book,
    chapter=None,
):
    """
    Store in-app notifications and schedule
    eligible push notifications after commit.
    """

    user_ids = list(
        recipients.values_list('id', flat=True)
    )

    if not user_ids:
        return recipients

    with transaction.atomic():
        notification_type = (
            get_publication_notification_type(
                type_code
            )
        )

        created_user_ids = (
            create_publication_notifications(
                user_ids=user_ids,
                notification_type=notification_type,
                title=title,
                message=message,
                book=book,
                chapter=chapter,
            )
        )

        if not created_user_ids:
            return recipients

        push_user_ids = get_push_enabled_user_ids(
            created_user_ids,
            notification_type,
        )

        if push_user_ids:
            data = {
                'type': type_code,
                'book_id': str(book.id),
            }

            if chapter is not None:
                data['chapter_id'] = str(chapter.id)

            def send_push():
                try:
                    send_expo_push_notifications(
                        user_ids=push_user_ids,
                        title=title,
                        body=message,
                        data=data,
                    )

                except Exception:
                    logger.exception(
                        'Failed to send publication push: %s',
                        type_code,
                    )

            transaction.on_commit(send_push)

    return recipients


def book_published(book):
    recipients = get_book_publication_recipients(book)

    author_profile = book.author_profile or book.free_author_profile

    author_name = (
        author_profile.pen_name
        if author_profile and author_profile.pen_name
        else 'an author you follow'
    )

    message = (
        f'A new book from {author_name} '
        f'is now available: {book.title}'
    )

    return publish_notification_event(
        recipients,
        'book_published',
        'New Book Published!',
        message,
        book,
    )


def chapter_published(chapter):
    recipients = get_chapter_publication_recipients(chapter)

    chapter_title = (chapter.title or '').strip()

    if chapter_title:
        chapter_name = chapter_title
    else:
        chapter_name = f'Chapter {chapter.chapter_number}'

    message = (
        f'{chapter_name} of {chapter.book.title} '
        'is now available!'
    )

    return publish_notification_event(
        recipients,
        'chapter_published',
        'New Chapter Available!',
        message,
        chapter.book,
        chapter,
    )
