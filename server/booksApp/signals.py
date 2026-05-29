from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

UNLOCK_COST_TABLE = {
    1: {'small': 5,  'medium': 20, 'large': 50},
    2: {'small': 10, 'medium': 25, 'large': 55},
    3: {'small': 15, 'medium': 30, 'large': 60},
    4: {'small': 20, 'medium': 35, 'large': 65},
    5: {'small': 25, 'medium': 40, 'large': 70},
}

def get_word_count_bucket(word_count):
    if word_count <= 1000:
        return 'small'
    elif word_count <= 2500:
        return 'medium'
    else:
        return 'large'

def calculate_unlock_cost(book, word_count):
    # free author books are always free
    if book.free_author_profile is not None and book.author_profile is None:
        return 0

    tier = book.book_tier
    if not tier:
        return 0

    bucket = get_word_count_bucket(word_count)
    return UNLOCK_COST_TABLE.get(tier, UNLOCK_COST_TABLE[1])[bucket]


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

    # auto-calculate unlock cost on create and content update
    # skip if chapter is free by chapter number (will be confirmed on publish via post_save)
    # but we can still set a provisional cost now for paid chapters
    if instance.book.book_tier and instance.status == 'draft':
        is_provisionally_free = instance.chapter_number and instance.chapter_number <= instance.book.free_chapters
        if not is_provisionally_free and not instance.is_free:
            instance.unlock_cost = calculate_unlock_cost(instance.book, instance.word_count)


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

        # recalculate unlock cost now that is_free is confirmed
        if is_free:
            Chapter.objects.filter(pk=instance.pk).update(unlock_cost=0)
        else:
            cost = calculate_unlock_cost(instance.book, instance.word_count)
            Chapter.objects.filter(pk=instance.pk).update(unlock_cost=cost)

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