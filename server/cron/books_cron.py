import logging
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger('cron')


def mark_books_not_new():
    from booksApp.models import Book
    from cronApp.models import CronLog

    try:
        cutoff = timezone.now() - timedelta(days=30)
        books = Book.objects.filter(
            is_new=True,
            created_at__lt=cutoff
        )
        count = books.count()
        books.update(is_new=False)

        message = f'Marked {count} books as not new'
        logger.info(message)
        print(message)

        CronLog.objects.create(
            job_name='mark_books_not_new',
            status='success',
            message=message,
            records_affected=count
        )

    except Exception as e:
        error_message = f'Error marking books as not new: {str(e)}'
        logger.error(error_message)
        CronLog.objects.create(
            job_name='mark_books_not_new',
            status='failure',
            message=error_message,
            records_affected=0
        )


def mark_chapters_not_new():
    from booksApp.models import Chapter
    from cronApp.models import CronLog

    try:
        cutoff = timezone.now() - timedelta(days=7)
        chapters = Chapter.objects.filter(
            is_new=True,
            published_at__lt=cutoff
        )
        count = chapters.count()
        chapters.update(is_new=False)

        message = f'Marked {count} chapters as not new'
        logger.info(message)
        print(message)

        CronLog.objects.create(
            job_name='mark_chapters_not_new',
            status='success',
            message=message,
            records_affected=count
        )

    except Exception as e:
        error_message = f'Error marking chapters as not new: {str(e)}'
        logger.error(error_message)
        CronLog.objects.create(
            job_name='mark_chapters_not_new',
            status='failure',
            message=error_message,
            records_affected=0
        )