from django.db import models
from userApp.models import AuthorProfile, FreeAuthorProfile


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ContentRating(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.code} - {self.name}'


class RelationshipTag(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Keyword(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('changes_requested', 'Changes Requested'),
        ('rejected', 'Rejected'),
    ]

    author_profile = models.ForeignKey(
        AuthorProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )
    free_author_profile = models.ForeignKey(
        FreeAuthorProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    cover_image = models.ImageField(
        upload_to='covers/',
        null=True,
        blank=True,
        default='covers/default.png'
    )
    content_rating = models.ForeignKey(
        ContentRating,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    book_tier = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_visible = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    is_complete = models.BooleanField(default=False)
    free_chapters = models.IntegerField(default=3)
    admin_notes = models.TextField(null=True, blank=True)
    reader_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BookPage(models.Model):
    PAGE_TYPES = [
        ('prologue', 'Prologue'),
        ('epilogue', 'Epilogue'),
        ('authors_note', "Author's Note"),
        ('dedication', 'Dedication'),
        ('acknowledgements', 'Acknowledgements'),
        ('next_book_teaser', 'Next Book Teaser'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='pages')
    page_type = models.CharField(max_length=20, choices=PAGE_TYPES)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('book', 'page_type')

    def __str__(self):
        return f'{self.book.title} - {self.page_type}'


class BookGenre(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'genre')

    def __str__(self):
        return f'{self.book.title} - {self.genre.name}'


class BookRelationshipTag(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='relationship_tags')
    tag = models.ForeignKey(RelationshipTag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'tag')

    def __str__(self):
        return f'{self.book.title} - {self.tag.name}'


class BookKeyword(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='keywords')
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'keyword')

    def __str__(self):
        return f'{self.book.title} - {self.keyword.name}'


class Chapter(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    chapter_number = models.IntegerField()
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_free = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    unlock_cost = models.IntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('book', 'chapter_number')
        ordering = ['chapter_number']

    def __str__(self):
        return f'{self.book.title} - Chapter {self.chapter_number}: {self.title}'


class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('userApp.User', on_delete=models.CASCADE, related_name='book_reviews')
    rating = models.IntegerField()
    body = models.TextField()
    flag_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return f'{self.user.email} review of {self.book.title}'


class ChapterComment(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('userApp.User', on_delete=models.CASCADE, related_name='chapter_comments')
    body = models.TextField()
    flag_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} comment on chapter {self.chapter.chapter_number}'


class UserBook(models.Model):
    user = models.ForeignKey('userApp.User', on_delete=models.CASCADE, related_name='user_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='user_books')
    completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f'{self.user.email} - {self.book.title}'


class UserReadingProgress(models.Model):
    UNLOCK_TYPES = [
        ('free', 'Free'),
        ('black_ink', 'Black Ink Drop'),
        ('gold_ink', 'Gold Ink Drop'),
        ('quills', 'Quills'),
    ]

    user = models.ForeignKey('userApp.User', on_delete=models.CASCADE, related_name='reading_progress')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_progress')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='reading_progress')
    is_unlocked = models.BooleanField(default=False)
    unlocked_at = models.DateTimeField(null=True, blank=True)
    unlock_currency_type = models.CharField(max_length=20, choices=UNLOCK_TYPES, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'chapter')

    def __str__(self):
        return f'{self.user.email} - {self.book.title} - Chapter {self.chapter.chapter_number}'