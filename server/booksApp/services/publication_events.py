
import logging

from django.contrib.auth import get_user_model
from django.db import transaction

from booksApp.models import UserBook
from booksApp.services.expo_push import (
    send_expo_push_notifications,
)


User = get_user_model()
logger = logging.getLogger(__name__)


def get_book_publication_recipients(book):
    """
    Return all users following the author who
    published this book.
    """

    if book.author_profile:
        user_ids = (
            book.author_profile
            .followers
            .values_list(
                'user_id',
                flat=True
            )
        )

        author_user_id = (
            book.author_profile.user_id
        )

    elif book.free_author_profile:
        user_ids = (
            book.free_author_profile
            .followers
            .values_list(
                'user_id',
                flat=True
            )
        )

        author_user_id = (
            book.free_author_profile.user_id
        )

    else:
        return User.objects.none()

    return (
        User.objects
        .filter(id__in=user_ids)
        .exclude(id=author_user_id)
        .distinct()
    )


def get_chapter_publication_recipients(chapter):
    """
    Return all users who currently have
    this book on their shelf.
    """

    user_ids = (
        UserBook.objects
        .filter(book=chapter.book)
        .values_list(
            'user_id',
            flat=True
        )
    )

    return (
        User.objects
        .filter(id__in=user_ids)
        .distinct()
    )


def book_published(book):
    """
    Notify followers when an author's book
    becomes publicly available for the first time.
    """

    recipients = get_book_publication_recipients(book)

    user_ids = list(
        recipients.values_list('id', flat=True)
    )

    if not user_ids:
        return recipients

    book_id = book.id
    book_title = str(book.title)

    def send_notification():
        try:
            send_expo_push_notifications(
                user_ids=user_ids,
                title="New Book Published!",
                body=(
                    f"A new book is available: "
                    f"{book_title}"
                ),
                data={
                    "type": "book_published",
                    "book_id": str(book_id),
                },
            )
        except Exception:
            logger.exception(
                "Failed to send book publication notification "
                "for book %s",
                book_id,
            )

    transaction.on_commit(send_notification)

    return recipients


def chapter_published(chapter):
    """
    Notify readers when a new chapter is
    published for a book on their shelf.
    """

    recipients = get_chapter_publication_recipients(
        chapter
    )

    user_ids = list(
        recipients.values_list('id', flat=True)
    )

    if not user_ids:
        return recipients

    chapter_id = chapter.id
    book_id = chapter.book_id
    book_title = str(chapter.book.title)
    chapter_title = str(chapter.title)

    def send_notification():
        try:
            send_expo_push_notifications(
                user_ids=user_ids,
                title="New Chapter Available!",
                body=(
                    f"{chapter_title} of "
                    f"{book_title} is now available!"
                ),
                data={
                    "type": "chapter_published",
                    "book_id": str(book_id),
                    "chapter_id": str(chapter_id),
                },
            )
        except Exception:
            logger.exception(
                "Failed to send chapter publication notification "
                "for chapter %s",
                chapter_id,
            )

    transaction.on_commit(send_notification)

    return recipients
