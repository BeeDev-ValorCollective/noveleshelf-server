from rest_framework import serializers
from booksApp.models import (
    Genre, ContentRating, RelationshipTag, Keyword,
    Book, BookPage, BookGenre, BookRelationshipTag, BookKeyword,
    Chapter, BookReview, ChapterComment,
    UserBook, UserReadingProgress
)
from currencyApp.serializers import FoundingAuthorBadgeSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


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
    display_title = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = [
            'id', 'chapter_number', 'title', 'display_title', 'status',
            'is_free', 'is_new', 'is_final', 'word_count', 'unlock_cost',
            'published_at', 'created_at', 'updated_at'
        ]

    def get_display_title(self, obj):
        if obj.title:
            return f'Chapter {obj.chapter_number}: {obj.title}'
        return f'Chapter {obj.chapter_number}'


class ChapterDetailSerializer(serializers.ModelSerializer):
    display_title = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = [
            'id', 'chapter_number', 'title', 'display_title', 'content',
            'status', 'is_free', 'is_new', 'is_final', 'word_count',
            'unlock_cost', 'published_at', 'created_at', 'updated_at'
        ]

    def get_display_title(self, obj):
        if obj.title:
            return f'Chapter {obj.chapter_number}: {obj.title}'
        return f'Chapter {obj.chapter_number}'


class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ['id', 'user', 'rating', 'body', 'flag_count', 'created_at', 'updated_at']


class ChapterCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChapterComment
        fields = ['id', 'user', 'body', 'flag_count', 'created_at', 'updated_at']


class BookSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    relationship_tags = serializers.SerializerMethodField()
    keywords = serializers.SerializerMethodField()
    content_rating = ContentRatingSerializer(read_only=True)
    pages = BookPageSerializer(many=True, read_only=True)
    chapters = ChapterSerializer(many=True, read_only=True)
    chapter_count = serializers.SerializerMethodField()
    published_chapter_count = serializers.SerializerMethodField()
    is_founding_eligible = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'cover_image', 'content_rating',
            'book_tier', 'status', 'is_visible', 'is_featured', 'is_new',
            'is_complete', 'free_chapters', 'has_pending_changes',
            'genres', 'relationship_tags', 'keywords', 'pages',
            'chapters', 'chapter_count', 'published_chapter_count',
            'is_founding_eligible', 'created_at', 'updated_at'
        ]

    def get_genres(self, obj):
        return GenreSerializer(
            [bg.genre for bg in obj.genres.select_related('genre').all()],
            many=True
        ).data

    def get_relationship_tags(self, obj):
        return RelationshipTagSerializer(
            [bt.tag for bt in obj.relationship_tags.select_related('tag').all()],
            many=True
        ).data

    def get_keywords(self, obj):
        return KeywordSerializer(
            [bk.keyword for bk in obj.keywords.select_related('keyword').all()],
            many=True
        ).data

    def get_chapter_count(self, obj):
        return obj.chapters.count()

    def get_published_chapter_count(self, obj):
        return obj.chapters.filter(status='published').count()

    def get_is_founding_eligible(self, obj):
        return obj.founding_author_eligibility.exists()

class BookAuthorAdminSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    pen_name = serializers.CharField()
    author_username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    show_real_name = serializers.BooleanField()
    author_type = serializers.CharField()

class BookAdminSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    relationship_tags = serializers.SerializerMethodField()
    keywords = serializers.SerializerMethodField()
    content_rating = ContentRatingSerializer(read_only=True)
    pages = BookPageSerializer(many=True, read_only=True)
    chapters = ChapterSerializer(many=True, read_only=True)
    chapter_count = serializers.SerializerMethodField()
    published_chapter_count = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    is_founding_eligible = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'cover_image', 'content_rating',
            'book_tier', 'status', 'is_visible', 'is_featured', 'is_new',
            'is_complete', 'free_chapters', 'has_pending_changes', 'submitted_at',
            'admin_notes', 'reader_notes', 'author', 'genres', 'relationship_tags',
            'keywords', 'pages', 'chapters', 'chapter_count',
            'published_chapter_count', 'is_founding_eligible', 'created_at', 'updated_at'
        ]

    def get_author(self, obj):
        profile = obj.author_profile or obj.free_author_profile
        if not profile:
            return {'id': None, 'email': '—', 'pen_name': None, 'author_username': None, 'first_name': None, 'last_name': None, 'show_real_name': False, 'author_type': 'unknown', 'founding_author': None}

        user = profile.user
        # Only paid AuthorProfile can hold a founding-author slot (free authors
        # are explicitly out of scope per the founding-author program design).
        founding_slot = getattr(profile, 'founding_author_slot', None) if obj.author_profile else None
        return {
            'id': user.id,
            'email': user.email,
            'pen_name': profile.pen_name,
            'author_username': profile.author_username,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'show_real_name': profile.show_real_name,
            'author_type': 'paid' if obj.author_profile else 'free',
            'founding_author': FoundingAuthorBadgeSerializer(founding_slot).data if founding_slot else None,
        }


    def get_genres(self, obj):
        return GenreSerializer(
            [bg.genre for bg in obj.genres.select_related('genre').all()],
            many=True
        ).data

    def get_relationship_tags(self, obj):
        return RelationshipTagSerializer(
            [bt.tag for bt in obj.relationship_tags.select_related('tag').all()],
            many=True
        ).data

    def get_keywords(self, obj):
        return KeywordSerializer(
            [bk.keyword for bk in obj.keywords.select_related('keyword').all()],
            many=True
        ).data

    def get_chapter_count(self, obj):
        return obj.chapters.count()

    def get_published_chapter_count(self, obj):
        return obj.chapters.filter(status='published').count()

    def get_is_founding_eligible(self, obj):
        return obj.founding_author_eligibility.exists()


class UserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBook
        fields = ['id', 'book', 'completion_percentage', 'is_completed', 'started_at', 'completed_at', 'last_read_at']


class UserReadingProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReadingProgress
        fields = ['id', 'book', 'chapter', 'is_unlocked', 'unlocked_at', 'unlock_currency_type', 'is_read', 'read_at']