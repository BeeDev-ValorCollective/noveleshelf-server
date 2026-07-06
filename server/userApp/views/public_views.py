from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from userApp.models import AuthorProfile, FreeAuthorProfile
from booksApp.models import Book
from booksApp.views.public_views import format_book_summary, get_visible_books


@api_view(['GET'])
@permission_classes([AllowAny])
def public_authors(request):
    featured_only = request.query_params.get('featured')

    paid_authors = AuthorProfile.objects.filter(
        is_publicly_visible=True,
        is_active=True,
        user__is_active=True,
    ).select_related('user')

    free_authors = FreeAuthorProfile.objects.filter(
        is_publicly_visible=True,
        is_active=True,
        user__is_active=True
    ).select_related('user')

    if featured_only and featured_only.lower() == 'true':
        paid_authors = paid_authors.filter(is_featured=True)
        free_authors = free_authors.filter(is_featured=True)

    authors_data = []

    for author in paid_authors:
        authors_data.append({
            'author_type': 'paid',
            'author_username': author.author_username,
            'display_name': f'{author.first_name} {author.last_name}' if author.show_real_name and author.first_name else author.pen_name or author.author_username,
            'pen_name': author.pen_name,
            'bio': author.bio,
            'avatar_url': author.avatar_url.url if author.avatar_url else None,
            'tier': author.tier,
            'is_featured': author.is_featured,
            'book_count': Book.objects.filter(
                author_profile=author,
                status='approved',
                is_visible=True
            ).count()
        })

    for author in free_authors:
        authors_data.append({
            'author_type': 'free',
            'author_username': author.author_username,
            'display_name': f'{author.first_name} {author.last_name}' if author.show_real_name and author.first_name else author.pen_name or author.author_username,
            'pen_name': author.pen_name,
            'bio': author.bio,
            'avatar_url': author.avatar_url.url if author.avatar_url else None,
            'tier': 'F2R',
            'is_featured': author.is_featured,
            'book_count': Book.objects.filter(
                free_author_profile=author,
                status='approved',
                is_visible=True
            ).count()

        })

    return Response({
        'count': len(authors_data),
        'authors': authors_data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def public_author_detail(request, username):
    # try paid first, then free
    profile = None
    author_type = None

    try:
        profile = AuthorProfile.objects.select_related('user').get(
            author_username=username,
            is_publicly_visible=True,
            is_active=True,
            user__is_active=True,
        )
        author_type = 'paid'
    except AuthorProfile.DoesNotExist:
        pass

    if not profile:
        try:
            profile = FreeAuthorProfile.objects.select_related('user').get(
                author_username=username,
                is_publicly_visible=True,
                is_active=True,
                user__is_active=True,
            )
            author_type = 'free'
        except FreeAuthorProfile.DoesNotExist:
            pass

    if not profile:
        return Response(
            {'error': 'Author not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # resolve display name
    if profile.show_real_name and profile.first_name:
        display_name = f'{profile.first_name} {profile.last_name or ""}'.strip()
    else:
        display_name = profile.pen_name or profile.author_username

    # founding author — paid only
    is_founding_author = getattr(profile, 'is_founding_author', False) if author_type == 'paid' else False

    # their published books
    if author_type == 'paid':
        books_qs = get_visible_books().filter(author_profile=profile).order_by('-created_at')
    else:
        books_qs = get_visible_books().filter(free_author_profile=profile).order_by('-created_at')

    author_data = {
        'id': profile.id,
        'author_type': author_type,
        'author_username': profile.author_username,
        'display_name': display_name,
        'pen_name': profile.pen_name,
        'bio': profile.bio,
        'avatar_url': profile.avatar_url.url if profile.avatar_url else None,
        'is_featured': profile.is_featured,
        'is_founding_author': is_founding_author,
        'book_count': books_qs.count(),
        'books': [format_book_summary(b) for b in books_qs],
    }

    return Response(author_data)