from rest_framework import serializers
from .models import (
    Genre, ContentRating, RelationshipTag, Keyword,
    Book, BookPage, BookGenre, BookRelationshipTag, BookKeyword,
    Chapter, BookReview, ChapterComment,
    UserBook, UserReadingProgress
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'is_active', 'created_at']


class ContentRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentRating
        fields = ['id', 'code', 'name', 'description', 'is_active']


class RelationshipTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationshipTag
        fields = ['id', 'code', 'name', 'is_active']


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['id', 'name', 'is_active']


class BookPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPage
        fields = ['id', 'page_type', 'content', 'is_published', 'created_at', 'updated_at']


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'chapter_number', 'title', 'status', 'is_free', 'is_new', 'unlock_cost', 'published_at', 'created_at', 'updated_at']


class ChapterDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'chapter_number', 'title', 'content', 'status', 'is_free', 'is_new', 'unlock_cost', 'published_at', 'created_at', 'updated_at']


class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ['id', 'user', 'rating', 'body', 'flag_count', 'created_at', 'updated_at']


class ChapterCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterComment
        fields = ['id', 'user', 'body', 'flag_count', 'created_at', 'updated_at']


class BookSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True, source='genres.all')
    relationship_tags = RelationshipTagSerializer(many=True, read_only=True, source='relationship_tags.all')
    keywords = KeywordSerializer(many=True, read_only=True, source='keywords.all')
    content_rating = ContentRatingSerializer(read_only=True)
    pages = BookPageSerializer(many=True, read_only=True)
    chapter_count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'cover_image', 'content_rating',
            'book_tier', 'status', 'is_visible', 'is_featured', 'is_new',
            'is_complete', 'free_chapters', 'genres', 'relationship_tags',
            'keywords', 'pages', 'chapter_count', 'created_at', 'updated_at'
        ]

    def get_chapter_count(self, obj):
        return obj.chapters.filter(status='published').count()


class BookAdminSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True, source='genres.all')
    relationship_tags = RelationshipTagSerializer(many=True, read_only=True, source='relationship_tags.all')
    keywords = KeywordSerializer(many=True, read_only=True, source='keywords.all')
    content_rating = ContentRatingSerializer(read_only=True)
    pages = BookPageSerializer(many=True, read_only=True)
    chapter_count = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'cover_image', 'content_rating',
            'book_tier', 'status', 'is_visible', 'is_featured', 'is_new',
            'is_complete', 'free_chapters', 'admin_notes', 'reader_notes',
            'genres', 'relationship_tags', 'keywords', 'pages',
            'chapter_count', 'created_at', 'updated_at'
        ]

    def get_chapter_count(self, obj):
        return obj.chapters.filter(status='published').count()


class UserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBook
        fields = ['id', 'book', 'completion_percentage', 'is_completed', 'started_at', 'completed_at', 'last_read_at']


class UserReadingProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReadingProgress
        fields = ['id', 'book', 'chapter', 'is_unlocked', 'unlocked_at', 'unlock_currency_type', 'is_read', 'read_at']