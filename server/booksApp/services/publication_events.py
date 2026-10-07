from django.contrib.auth import get_user_model

from booksApp.models import UserBook


User = get_user_model()


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


def get_chapter_publication_recipients(
    chapter
):
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
    Called when a book becomes publicly
    available for the first time.

    Delivery method will be added later.
    """

    recipients = (
        get_book_publication_recipients(
            book
        )
    )

    return recipients


def chapter_published(chapter):
    """
    Called when a chapter is published
    for the first time.

    Delivery method will be added later.
    """

    recipients = (
        get_chapter_publication_recipients(
            chapter
        )
    )

    return recipients
