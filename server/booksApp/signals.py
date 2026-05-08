from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(pre_save, sender='booksApp.Chapter')
def handle_chapter_pre_save(sender, instance, **kwargs):
    # auto-increment chapter_number on create
    if not instance.pk:
        from .models import Chapter
        last_chapter = Chapter.objects.filter(
            book=instance.book
        ).order_by('chapter_number').last()
        instance.chapter_number = (last_chapter.chapter_number + 1) if last_chapter else 1

    # auto-calculate word count
    if instance.content:
        instance.word_count = len(instance.content.split())


@receiver(post_save, sender='booksApp.Chapter')
def handle_chapter_post_save(sender, instance, created, **kwargs):
    from .models import Chapter, Book

    # when chapter is published for the first time
    if instance.status == 'published' and instance.published_at is None:
        # set published_at
        Chapter.objects.filter(pk=instance.pk).update(published_at=timezone.now())

        # set is_free based on chapter number vs book free_chapters
        is_free = instance.chapter_number <= instance.book.free_chapters
        Chapter.objects.filter(pk=instance.pk).update(is_free=is_free)

        # set book is_new to True when first chapter published
        if instance.chapter_number == 1:
            instance.book.is_new = True
            instance.book.save()

    # if is_final is marked, set book is_complete — permanent once set
    if instance.is_final and not instance.book.is_complete:
        Book.objects.filter(pk=instance.book.pk).update(is_complete=True)


@receiver(post_save, sender='booksApp.UserReadingProgress')
def handle_reading_progress(sender, instance, created, **kwargs):
    from .models import UserBook, UserReadingProgress

    if instance.is_read:
        # update or create UserBook entry
        user_book, _ = UserBook.objects.get_or_create(
            user=instance.user,
            book=instance.book
        )

        # update last read at
        user_book.last_read_at = timezone.now()

        # calculate completion percentage
        total_published = instance.book.chapters.filter(status='published').count()
        total_read = UserReadingProgress.objects.filter(
            user=instance.user,
            book=instance.book,
            is_read=True
        ).count()

        if total_published > 0:
            user_book.completion_percentage = round((total_read / total_published) * 100, 2)

        # check if book is complete and all chapters read
        if instance.book.is_complete and user_book.completion_percentage == 100:
            user_book.is_completed = True
            user_book.completed_at = timezone.now()

        user_book.save()