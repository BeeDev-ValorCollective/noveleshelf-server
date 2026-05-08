from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from booksApp.models import (
    Book, BookPage, BookGenre, BookRelationshipTag, BookKeyword,
    Chapter, Genre, ContentRating, RelationshipTag, Keyword
)
from booksApp.serializers import (
    BookSerializer, ChapterSerializer,
    ChapterDetailSerializer, BookPageSerializer,
    GenreSerializer, ContentRatingSerializer,
    RelationshipTagSerializer, KeywordSerializer
)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_active_author_profile(user, author_type):
    """
    Returns (profile, profile_type) based on author_type passed in request.
    If user only has one profile type, author_type is optional.
    Returns (None, None) if profile not found.
    """
    has_paid = hasattr(user, 'author_profile')
    has_free = hasattr(user, 'free_author_profile')

    if not has_paid and not has_free:
        return None, None

    # if user only has one profile type, use it regardless of author_type
    if has_paid and not has_free:
        return user.author_profile, 'paid'
    if has_free and not has_paid:
        return user.free_author_profile, 'free'

    # user has both — author_type is required
    if not author_type:
        return None, 'both'

    if author_type == 'paid':
        return user.author_profile, 'paid'
    elif author_type == 'free':
        return user.free_author_profile, 'free'

    return None, None


def get_book_for_author(book_id, user, author_type):
    """
    Returns book if it belongs to the user's active author profile.
    Returns None if not found or not owned by user.
    """
    profile, profile_type = get_active_author_profile(user, author_type)

    if not profile:
        return None, profile_type

    try:
        if profile_type == 'paid':
            return Book.objects.get(id=book_id, author_profile=profile), profile_type
        else:
            return Book.objects.get(id=book_id, free_author_profile=profile), profile_type
    except Book.DoesNotExist:
        return None, profile_type


def author_type_error_response():
    return Response(
        {'error': 'author_type is required when you have both paid and free author profiles. Must be paid or free.'},
        status=status.HTTP_400_BAD_REQUEST
    )


def not_author_error_response():
    return Response(
        {'error': 'You must be an author to perform this action'},
        status=status.HTTP_403_FORBIDDEN
    )


# ─── Book Management ──────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_book(request):
    author_type = request.data.get('author_type')
    profile, profile_type = get_active_author_profile(request.user, author_type)

    if profile_type == 'both':
        return author_type_error_response()

    if not profile:
        return not_author_error_response()

    title = request.data.get('title')

    if not title:
        return Response(
            {'error': 'title is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    description = request.data.get('description')
    cover_image = request.data.get('cover_image')
    content_rating_id = request.data.get('content_rating_id')
    free_chapters = request.data.get('free_chapters')

    content_rating = None
    if content_rating_id:
        try:
            content_rating = ContentRating.objects.get(id=content_rating_id, is_active=True)
        except ContentRating.DoesNotExist:
            return Response(
                {'error': 'Content rating not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    if profile_type == 'paid':
        book = Book(
            author_profile=profile,
            title=title,
            description=description,
            content_rating=content_rating,
            status='draft',
            cover_image=cover_image if cover_image else 'bookCovers/paid/default.png'
        )
    else:
        book = Book(
            free_author_profile=profile,
            title=title,
            description=description,
            content_rating=content_rating,
            status='approved',
            cover_image=cover_image if cover_image else 'bookCovers/free/default.png'
        )

    if free_chapters is not None:
        try:
            book.free_chapters = int(free_chapters)
        except ValueError:
            return Response(
                {'error': 'free_chapters must be a number'},
                status=status.HTTP_400_BAD_REQUEST
            )

    book.save()

    return Response({
        'message': f'Book "{book.title}" created successfully',
        'book': BookSerializer(book).data
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_my_books(request):
    author_type = request.query_params.get('author_type')
    profile, profile_type = get_active_author_profile(request.user, author_type)

    if profile_type == 'both':
        return author_type_error_response()

    if not profile:
        return not_author_error_response()

    if profile_type == 'paid':
        books = Book.objects.filter(author_profile=profile).order_by('-created_at')
    else:
        books = Book.objects.filter(free_author_profile=profile).order_by('-created_at')

    status_filter = request.query_params.get('status')
    if status_filter:
        books = books.filter(status=status_filter)

    return Response({
        'count': books.count(),
        'books': BookSerializer(books, many=True).data
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_book(request):
    author_type = request.data.get('author_type')
    profile, profile_type = get_active_author_profile(request.user, author_type)

    if profile_type == 'both':
        return author_type_error_response()

    if not profile:
        return not_author_error_response()

    book_id = request.data.get('book_id')

    if not book_id:
        return Response(
            {'error': 'book_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    book, _ = get_book_for_author(book_id, request.user, author_type)

    if not book:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if book.status == 'rejected':
        return Response(
            {'error': 'Rejected books cannot be edited'},
            status=status.HTTP_400_BAD_REQUEST
        )

    title = request.data.get('title')
    description = request.data.get('description')
    cover_image = request.data.get('cover_image')
    content_rating_id = request.data.get('content_rating_id')
    free_chapters = request.data.get('free_chapters')

    if title is not None:
        book.title = title

    if description is not None:
        book.description = description

    if cover_image:
        book.cover_image = cover_image

    if content_rating_id is not None:
        try:
            book.content_rating = ContentRating.objects.get(id=content_rating_id, is_active=True)
        except ContentRating.DoesNotExist:
            return Response(
                {'error': 'Content rating not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    if free_chapters is not None:
        try:
            book.free_chapters = int(free_chapters)
        except ValueError:
            return Response(
                {'error': 'free_chapters must be a number'},
                status=status.HTTP_400_BAD_REQUEST
            )

    if book.status == 'pending_approval':
        book.has_pending_changes = True

    book.save()

    return Response({
        'message': f'Book "{book.title}" updated successfully',
        'book': BookSerializer(book).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_book(request):
    author_type = request.data.get('author_type')
    profile, profile_type = get_active_author_profile(request.user, author_type)

    if profile_type == 'both':
        return author_type_error_response()

    if not profile or profile_type != 'paid':
        return Response(
            {'error': 'Only paid authors can submit books for approval'},
            status=status.HTTP_403_FORBIDDEN
        )

    book_id = request.data.get('book_id')

    if not book_id:
        return Response(
            {'error': 'book_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    book, _ = get_book_for_author(book_id, request.user, author_type)

    if not book:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if book.status not in ['draft', 'changes_requested']:
        return Response(
            {'error': f'Books with status "{book.status}" cannot be submitted for approval'},
            status=status.HTTP_400_BAD_REQUEST
        )

    book.status = 'pending_approval'
    book.submitted_at = timezone.now()
    book.has_pending_changes = False
    book.save()

    return Response({
        'message': f'Book "{book.title}" submitted for approval successfully',
        'book': BookSerializer(book).data
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_book(request):
    author_type = request.data.get('author_type')
    profile, profile_type = get_active_author_profile(request.user, author_type)

    if profile_type == 'both':
        return author_type_error_response()

    if not profile:
        return not_author_error_response()

    book_id = request.data.get('book_id')

    if not book_id:
        return Response(
            {'error': 'book_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    book, _ = get_book_for_author(book_id, request.user, author_type)

    if not book:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if book.chapters.filter(status='published').exists():
        return Response(
            {'error': 'Books with published chapters cannot be deleted'},
            status=status.HTTP_400_BAD_REQUEST
        )

    book_title = book.title
    book.delete()

    return Response({
        'message': f'Book "{book_title}" deleted successfully'
    })


# ─── Genre / Tag / Keyword Management ────────────────────────────────────────

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_genre(request):
    author_type = request.data.get('author_type')
    profile, profile_type = get_active_author_profile(request.user, author_type)

    if profile_type == 'both':
        return author_type_error_response()

    if not profile:
        return not_author_error_response()

    book_id = request.data.get('book_id')
    genre_id = request.data.get('genre_id')

    if not book_id or not genre_id:
        return Response(
            {'error': 'book_id and genre_id are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    book, _ = get_book_for_author(book_id, request.user, author_type)

    if not book:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        genre = Genre.objects.get(id=genre_id, is_active=True)
    except Genre.DoesNotExist:
        return Response(
            {'error': 'Genre not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if BookGenre.objects.filter(book=book, genre=genre).exists():
        return Response(
            {'error': 'This genre is already added to the book'},
            status=status.HTTP_400_BAD_REQUEST
        )

    BookGenre.objects.create(book=book, genre=genre)

    return Response({
        'message': f'Genre "{genre.name}" added to "{book.title}" successfully',
        'book': BookSerializer(book).data
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_genre(request):
    author_type = request.data.get('author_type')
    profile, profile_type = get_active_author_profile(request.user, author_type)

    if profile_type == 'both':
        return author_type_error_response()

    if not profile:
        return not_author_error_response()

    book_id = request.data.get('book_id')
    genre_id = request.data.get('genre_id')

    if not book_id or not genre_id:
        return Response(
            {'error': 'book_id and genre_id are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    book, _ = get_book_for_author(book_id, request.user, author_type)

    if not book:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        book_genre = BookGenre.objects.get(book=book, genre_id=genre_id)
    except BookGenre.DoesNotExist:
        return Response(
            {'error': 'Genre not found on this book'},
            status=status.HTTP_404_NOT_FOUND
        )

    book_genre.delete()

    return Response({
        'message': 'Genre removed successfully',
        'book': BookSerializer(book).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_relationship_tag(request):
    author_type = request.data.get('author_type')
    profile, profile_type = get_active_author_profile(request.user, author_type)

    if profile_type == 'both':
        return author_type_error_response()

    if not profile:
        return not_author_error_response()

    book_id = request.data.get('book_id')
    tag_id = request.data.get('tag_id')

    if not book_id or not tag_id:
        return Response(
            {'error': 'book_id and tag_id are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    book, _ = get_book_for_author(book_id, request.user, author_type)

    if not book:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        tag = RelationshipTag.objects.get(id=tag_id, is_active=True)
    except RelationshipTag.DoesNotExist:
        return Response(
            {'error': 'Relationship tag not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if BookRelationshipTag.objects.filter(book=book, tag=tag).exists():
        return Response(
            {'error': 'This tag is already added to the book'},
            status=status.HTTP_400_BAD_REQUEST
        )

    BookRelationshipTag.objects.create(book=book, tag=tag)

    return Response({
        'message': f'Tag "{tag.name}" added to "{book.title}" successfully',
        'book': BookSerializer(book).data
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_relationship_tag(request):
    author_type = request.data.get('author_type')
    profile, profile_type = get_active_author_profile(request.user, author_type)

    if profile_type == 'both':
        return author_type_error_response()

    if not profile:
        return not_author_error_response()

    book_id = request.data.get('book_id')
    tag_id = request.data.get('tag_id')

    if not book_id or not tag_id:
        return Response(
            {'error': 'book_id and tag_id are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    book, _ = get_book_for_author(book_id, request.user, author_type)

    if not book:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        book_tag = BookRelationshipTag.objects.get(book=book, tag_id=tag_id)
    except BookRelationshipTag.DoesNotExist:
        return Response(
            {'error': 'Tag not found on this book'},
            status=status.HTTP_404_NOT_FOUND
        )

    book_tag.delete()

    return Response({
        'message': 'Tag removed successfully',
        'book': BookSerializer(book).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_keyword(request):
    author_type = request.data.get('author_type')
    profile, profile_type = get_active_author_profile(request.user, author_type)

    if profile_type == 'both':
        return author_type_error_response()

    if not profile:
        return not_author_error_response()

    book_id = request.data.get('book_id')
    keyword_id = request.data.get('keyword_id')

    if not book_id or not keyword_id:
        return Response(
            {'error': 'book_id and keyword_id are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    book, _ = get_book_for_author(book_id, request.user, author_type)

    if not book:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        keyword = Keyword.objects.get(id=keyword_id, is_active=True)
    except Keyword.DoesNotExist:
        return Response(
            {'error': 'Keyword not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if BookKeyword.objects.filter(book=book, keyword=keyword).exists():
        return Response(
            {'error': 'This keyword is already added to the book'},
            status=status.HTTP_400_BAD_REQUEST
        )

    BookKeyword.objects.create(book=book, keyword=keyword)

    return Response({
        'message': f'Keyword "{keyword.name}" added to "{book.title}" successfully',
        'book': BookSerializer(book).data
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_keyword(request):
    author_type = request.data.get('author_type')
    profile, profile_type = get_active_author_profile(request.user, author_type)

    if profile_type == 'both':
        return author_type_error_response()

    if not profile:
        return not_author_error_response()

    book_id = request.data.get('book_id')
    keyword_id = request.data.get('keyword_id')

    if not book_id or not keyword_id:
        return Response(
            {'error': 'book_id and keyword_id are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    book, _ = get_book_for_author(book_id, request.user, author_type)

    if not book:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        book_keyword = BookKeyword.objects.get(book=book, keyword_id=keyword_id)
    except BookKeyword.DoesNotExist:
        return Response(
            {'error': 'Keyword not found on this book'},
            status=status.HTTP_404_NOT_FOUND
        )

    book_keyword.delete()

    return Response({
        'message': 'Keyword removed successfully',
        'book': BookSerializer(book).data
    })