# booksApp - public_views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from booksApp.models import Book, BookPage, Chapter, Genre, RelationshipTag, Keyword, ContentRating
from userApp.models import AuthorProfile, FreeAuthorProfile
from booksApp.serializers import GenreSerializer, KeywordSerializer, RelationshipTagSerializer, ContentRatingSerializer


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_author_display(book):
    """Returns display name and profile info for a book's author."""
    if book.author_profile:
        profile = book.author_profile
        if profile.show_real_name and profile.first_name:
            name = f'{profile.first_name} {profile.last_name or ""}'.strip()
        else:
            name = profile.pen_name or profile.author_username or profile.user.email
        return {
            'display_name': name,
            'username': profile.author_username,
            'avatar_url': str(profile.avatar_url) if profile.avatar_url else None,
            'is_featured': profile.is_featured,
            'author_type': 'paid'
        }
    elif book.free_author_profile:
        profile = book.free_author_profile
        if profile.show_real_name and profile.first_name:
            name = f'{profile.first_name} {profile.last_name or ""}'.strip()
        else:
            name = profile.pen_name or profile.author_username or profile.user.email
        return {
            'display_name': name,
            'username': profile.author_username,
            'avatar_url': str(profile.avatar_url) if profile.avatar_url else None,
            'is_featured': profile.is_featured,
            'author_type': 'free'
        }
    return None


def get_display_name(profile, author_type):
    """Shared display name resolution for author profiles."""
    if profile.show_real_name and profile.first_name:
        return f'{profile.first_name} {profile.last_name or ""}'.strip()
    return profile.pen_name or profile.author_username or profile.user.email


def format_book_summary(book):
    """Returns summary card data for a book."""
    description = book.description or ''
    truncated = len(description) > 150
    author = get_author_display(book)

    return {
        'id': book.id,
        'title': book.title,
        'cover_image': book.cover_image.url if book.cover_image else None,
        'description': description[:150] if truncated else description,
        'description_truncated': truncated,
        'content_rating': {
            'code': book.content_rating.code,
            'name': book.content_rating.name,
        } if book.content_rating else None,
        'book_tier': book.book_tier,
        'is_complete': book.is_complete,
        'is_new': book.is_new,
        'is_featured': book.is_featured,
        'is_founding_eligible': book.founding_author_eligibility.exists(),
        'chapter_count': book.chapters.count(),
        'published_chapter_count': book.chapters.filter(status='published').count(),
        'genres': [{'id': g.genre.id, 'name': g.genre.name} for g in book.genres.all()],
        'relationship_tags': [{'id': t.tag.id, 'code': t.tag.code, 'name': t.tag.name} for t in book.relationship_tags.all()],
        'keywords': [{'id': k.keyword.id, 'name': k.keyword.name} for k in book.keywords.all()],
        'author': author,
    }


def format_author_summary(profile, author_type):
    """Returns summary card data for an author."""
    name = get_display_name(profile, author_type)
    is_founding = getattr(profile, 'is_founding_author', False) if author_type == 'paid' else False

    if author_type == 'paid':
        book_count = Book.objects.filter(
            author_profile=profile,
            status='approved',
            is_visible=True
        ).count()
    else:
        book_count = Book.objects.filter(
            free_author_profile=profile,
            status='approved',
            is_visible=True
        ).count()

    return {
        'id': profile.id,
        'display_name': name,
        'username': profile.author_username,
        'avatar_url': profile.avatar_url.url if profile.avatar_url else None,
        'bio': profile.bio,
        'is_featured': profile.is_featured,
        'is_founding_author': is_founding,
        'author_type': author_type,
        'book_count': book_count,
    }


def get_visible_books():
    """Base queryset for all publicly visible books."""
    return Book.objects.filter(
        status='approved',
        is_visible=True
    ).select_related(
        'content_rating',
        'author_profile',
        'author_profile__user',
        'free_author_profile',
        'free_author_profile__user',
    ).prefetch_related(
        'genres__genre',
        'relationship_tags__tag',
        'keywords__keyword',
    )


def get_visible_authors():
    """Returns (paid_qs, free_qs) for all publicly visible authors."""
    paid = AuthorProfile.objects.filter(
        is_publicly_visible=True,
        is_active=True,
    ).select_related('user')

    free = FreeAuthorProfile.objects.filter(
        is_publicly_visible=True,
        is_active=True,
    ).select_related('user')

    return paid, free


# ─── Featured ─────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def featured(request):
    featured_books = get_visible_books().filter(is_featured=True).order_by('-updated_at')[:6]

    paid_authors = AuthorProfile.objects.filter(
        is_featured=True,
        is_publicly_visible=True
    ).select_related('user')[:4]

    free_authors = FreeAuthorProfile.objects.filter(
        is_featured=True,
        is_publicly_visible=True
    ).select_related('user')

    authors = []
    for profile in paid_authors:
        authors.append(format_author_summary(profile, 'paid'))

    for profile in free_authors:
        if len(authors) >= 4:
            break
        authors.append(format_author_summary(profile, 'free'))

    return Response({
        'featured_books': [format_book_summary(b) for b in featured_books],
        'featured_authors': authors,
    })


# ─── Book / Author List ───────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def book_list(request):
    view = request.query_params.get('view', 'books')

    if view == 'authors':
        return author_list(request)

    # ── Books ──
    books = get_visible_books()

    search = request.query_params.get('search')
    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author_profile__pen_name__icontains=search) |
            Q(author_profile__author_username__icontains=search) |
            Q(author_profile__first_name__icontains=search) |
            Q(author_profile__last_name__icontains=search) |
            Q(free_author_profile__pen_name__icontains=search) |
            Q(free_author_profile__author_username__icontains=search) |
            Q(genres__genre__name__icontains=search) |
            Q(keywords__keyword__name__icontains=search) |
            Q(relationship_tags__tag__name__icontains=search)
        ).distinct()

    genre = request.query_params.get('genre')
    if genre:
        books = books.filter(genres__genre__id=genre)

    relationship_tag = request.query_params.get('relationship_tag')
    if relationship_tag:
        books = books.filter(relationship_tags__tag__id=relationship_tag)

    keyword = request.query_params.get('keyword')
    if keyword:
        books = books.filter(keywords__keyword__id=keyword)

    content_rating = request.query_params.get('content_rating')
    if content_rating:
        books = books.filter(content_rating__id=content_rating)

    is_featured = request.query_params.get('is_featured')
    if is_featured is not None:
        books = books.filter(is_featured=is_featured.lower() == 'true')

    is_new = request.query_params.get('is_new')
    if is_new is not None:
        books = books.filter(is_new=is_new.lower() == 'true')

    is_complete = request.query_params.get('is_complete')
    if is_complete is not None:
        books = books.filter(is_complete=is_complete.lower() == 'true')

    # ordering
    order = request.query_params.get('order', 'newest')
    if order == 'az':
        books = books.order_by('title')
    elif order == 'za':
        books = books.order_by('-title')
    elif order == 'featured':
        books = books.order_by('-is_featured', '-created_at')
    else:
        books = books.order_by('-created_at')

    # pagination
    try:
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 12))
    except ValueError:
        page = 1
        page_size = 12

    page_size = min(page_size, 50)
    start = (page - 1) * page_size
    end = start + page_size

    total = books.count()
    books_page = books[start:end]

    return Response({
        'view': 'books',
        'count': total,
        'page': page,
        'page_size': page_size,
        'total_pages': -(-total // page_size),
        'results': [format_book_summary(b) for b in books_page],
    })


def author_list(request):
    """Inner handler for ?view=authors — called from book_list."""
    paid_qs, free_qs = get_visible_authors()

    search = request.query_params.get('search')
    if search:
        paid_qs = paid_qs.filter(
            Q(pen_name__icontains=search) |
            Q(author_username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(bio__icontains=search)
        )
        free_qs = free_qs.filter(
            Q(pen_name__icontains=search) |
            Q(author_username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(bio__icontains=search)
        )

    is_featured = request.query_params.get('is_featured')
    if is_featured is not None:
        featured_val = is_featured.lower() == 'true'
        paid_qs = paid_qs.filter(is_featured=featured_val)
        free_qs = free_qs.filter(is_featured=featured_val)

    # founding filter only applies to paid authors
    is_founding = request.query_params.get('is_founding_author')
    if is_founding is not None:
        founding_val = is_founding.lower() == 'true'
        paid_qs = paid_qs.filter(is_founding_author=founding_val)
        if founding_val:
            free_qs = free_qs.none()

    # build combined list
    authors = []
    for profile in paid_qs:
        authors.append(format_author_summary(profile, 'paid'))
    for profile in free_qs:
        authors.append(format_author_summary(profile, 'free'))

    # ordering
    order = request.query_params.get('order', 'az')
    if order == 'za':
        authors.sort(key=lambda a: a['display_name'].lower(), reverse=True)
    elif order == 'featured':
        authors.sort(key=lambda a: (not a['is_featured'], a['display_name'].lower()))
    else:
        authors.sort(key=lambda a: a['display_name'].lower())

    # pagination
    try:
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 12))
    except ValueError:
        page = 1
        page_size = 12

    page_size = min(page_size, 50)
    total = len(authors)
    start = (page - 1) * page_size
    end = start + page_size

    return Response({
        'view': 'authors',
        'count': total,
        'page': page,
        'page_size': page_size,
        'total_pages': -(-total // page_size),
        'results': authors[start:end],
    })


# ─── Book Detail ──────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def book_detail(request, book_id):
    try:
        book = get_visible_books().get(id=book_id)
    except Book.DoesNotExist:
        return Response(
            {'error': 'Book not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    pages = BookPage.objects.filter(
        book=book,
        is_published=True
    ).values('id', 'page_type', 'content')

    chapters = Chapter.objects.filter(
        book=book,
        status='published'
    ).order_by('chapter_number').values(
        'id', 'chapter_number', 'title',
        'is_free', 'is_new', 'is_final', 'word_count',
        'unlock_cost', 'published_at'
    )

    chapters_data = []
    for chapter in chapters:
        chapter['display_title'] = f'Chapter {chapter["chapter_number"]}: {chapter["title"]}' if chapter['title'] else f'Chapter {chapter["chapter_number"]}'
        chapters_data.append(chapter)

    data = format_book_summary(book)
    data['description'] = book.description or ''
    data['description_truncated'] = False
    data['pages'] = list(pages)
    data['chapters'] = chapters_data

    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def book_reference_data(request):
    return Response({
        'genres': GenreSerializer(Genre.objects.filter(is_active=True), many=True).data,
        'keywords': KeywordSerializer(Keyword.objects.filter(is_active=True), many=True).data,
        'relationship_tags': RelationshipTagSerializer(RelationshipTag.objects.filter(is_active=True), many=True).data,
        'content_ratings': ContentRatingSerializer(ContentRating.objects.all(), many=True).data,
    })