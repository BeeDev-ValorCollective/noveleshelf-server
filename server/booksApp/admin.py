from django.contrib import admin
from .models import (
    Genre, ContentRating, RelationshipTag, Keyword,
    Book, BookPage, BookGenre, BookRelationshipTag, BookKeyword,
    Chapter, BookReview, ChapterComment,
    UserBook, UserReadingProgress
)


class BookGenreInline(admin.TabularInline):
    model = BookGenre
    extra = 1


class BookRelationshipTagInline(admin.TabularInline):
    model = BookRelationshipTag
    extra = 1


class BookKeywordInline(admin.TabularInline):
    model = BookKeyword
    extra = 1


class BookPageInline(admin.StackedInline):
    model = BookPage
    extra = 0


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0
    fields = ['chapter_number', 'title', 'status', 'is_free', 'is_new', 'unlock_cost', 'published_at']
    readonly_fields = ['published_at']


class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_profile', 'free_author_profile', 'status', 'is_visible', 'is_featured', 'is_new', 'is_complete', 'book_tier', 'created_at']
    list_filter = ['status', 'is_visible', 'is_featured', 'is_new', 'is_complete']
    search_fields = ['title']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [BookGenreInline, BookRelationshipTagInline, BookKeywordInline, BookPageInline, ChapterInline]


class ChapterAdmin(admin.ModelAdmin):
    list_display = ['book', 'chapter_number', 'title', 'status', 'is_free', 'is_new', 'unlock_cost', 'published_at']
    list_filter = ['status', 'is_free', 'is_new']
    search_fields = ['title', 'book__title']
    readonly_fields = ['published_at', 'created_at', 'updated_at']


class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'flag_count', 'created_at']
    list_filter = ['rating', 'flag_count']
    search_fields = ['book__title', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


class ChapterCommentAdmin(admin.ModelAdmin):
    list_display = ['chapter', 'user', 'flag_count', 'created_at']
    list_filter = ['flag_count']
    search_fields = ['chapter__title', 'user__email']
    readonly_fields = ['created_at', 'updated_at']


class UserBookAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'completion_percentage', 'is_completed', 'started_at', 'last_read_at']
    list_filter = ['is_completed']
    search_fields = ['user__email', 'book__title']
    readonly_fields = ['started_at', 'completed_at', 'last_read_at']


class ContentRatingAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active']
    list_filter = ['is_active']


class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']


class RelationshipTagAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active']
    list_filter = ['is_active']


class KeywordAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']


admin.site.register(Genre, GenreAdmin)
admin.site.register(ContentRating, ContentRatingAdmin)
admin.site.register(RelationshipTag, RelationshipTagAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookPage)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(BookReview, BookReviewAdmin)
admin.site.register(ChapterComment, ChapterCommentAdmin)
admin.site.register(UserBook, UserBookAdmin)
admin.site.register(UserReadingProgress)