from rest_framework import serializers
from booksApp.models import UserBook, UserReadingProgress, Chapter, Book
from userApp.models import AuthorProfile, FreeAuthorProfile


class LibraryAuthorSerializer(serializers.Serializer):
    """Minimal author info for library card display."""
    author_username = serializers.CharField()
    pen_name = serializers.CharField()
    avatar_url = serializers.ImageField()


class LibraryBookSerializer(serializers.ModelSerializer):
    """Book info needed to render a shelf card — no second call needed."""
    cover_image = serializers.ImageField()
    author = serializers.SerializerMethodField()
    genre_list = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'cover_image', 'author', 'genre_list', 'is_complete', 'book_tier']

    def get_author(self, obj):
        if obj.author_profile:
            return {
                'author_username': obj.author_profile.author_username,
                'pen_name': obj.author_profile.pen_name,
                'avatar_url': self.context['request'].build_absolute_uri(obj.author_profile.avatar_url.url) if obj.author_profile.avatar_url else None,
            }
        if obj.free_author_profile:
            return {
                'author_username': obj.free_author_profile.author_username,
                'pen_name': obj.free_author_profile.pen_name,
                'avatar_url': self.context['request'].build_absolute_uri(obj.free_author_profile.avatar_url.url) if obj.free_author_profile.avatar_url else None,
            }
        return None

    def get_genre_list(self, obj):
        return list(obj.genres.filter(genre__is_active=True).values_list('genre__name', flat=True))


class UserBookSerializer(serializers.ModelSerializer):
    """Full library entry — book card + progress in one."""
    book = LibraryBookSerializer(read_only=True)

    class Meta:
        model = UserBook
        fields = [
            'id', 'book', 'completion_percentage', 'is_completed',
            'started_at', 'completed_at', 'last_read_at'
        ]


class ChapterReadSerializer(serializers.ModelSerializer):
    """Chapter content for reading view."""
    book_title = serializers.CharField(source='book.title', read_only=True)
    total_chapters = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = [
            'id', 'chapter_number', 'title', 'content',
            'word_count', 'is_free', 'unlock_cost',
            'is_final', 'book_title', 'total_chapters',
            'published_at'
        ]

    def get_total_chapters(self, obj):
        return obj.book.chapters.filter(status='published').count()


class ChapterLockedSerializer(serializers.ModelSerializer):
    """Returned when chapter needs unlocking — no content, just cost info."""
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Chapter
        fields = [
            'id', 'chapter_number', 'title',
            'unlock_cost', 'book_title', 'word_count'
        ]