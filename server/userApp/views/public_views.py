from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from userApp.models import AuthorProfile, FreeAuthorProfile


@api_view(['GET'])
@permission_classes([AllowAny])
def public_authors(request):
    featured_only = request.query_params.get('featured')
    
    # paid authors
    paid_authors = AuthorProfile.objects.filter(
        is_publicly_visible=True,
        is_active=True,
        user__is_active=True,
    ).select_related('user')

    # free authors
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
        })

    return Response({
        'count': len(authors_data),
        'authors': authors_data
    })