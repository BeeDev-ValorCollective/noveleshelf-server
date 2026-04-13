from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import AuthorProfile


@api_view(['GET'])
@permission_classes([AllowAny])
def public_authors(request):
    authors = AuthorProfile.objects.filter(
        is_publicly_visible=True,
        user__is_active=True
    ).select_related('user')

    authors_data = []
    for author in authors:
        authors_data.append({
            'author_username': author.author_username,
            'display_name': f'{author.first_name} {author.last_name}' if author.show_real_name and author.first_name else author.pen_name or author.author_username,
            'pen_name': author.pen_name,
            'bio': author.bio,
            'avatar_url': author.avatar_url.url if author.avatar_url else None,
            'tier': author.tier,
        })

    return Response({
        'count': len(authors_data),
        'authors': authors_data
    })