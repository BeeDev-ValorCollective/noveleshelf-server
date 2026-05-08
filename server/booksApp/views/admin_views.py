# booksApp - admin_views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from booksApp.models import Genre, ContentRating, RelationshipTag, Keyword
from booksApp.serializers import GenreSerializer, ContentRatingSerializer, RelationshipTagSerializer, KeywordSerializer


# ─── Genre ────────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_genres(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    is_active = request.query_params.get('is_active')
    genres = Genre.objects.all().order_by('name')

    if is_active is not None:
        genres = genres.filter(is_active=is_active.lower() == 'true')

    return Response({
        'count': genres.count(),
        'genres': GenreSerializer(genres, many=True).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_genre(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    name = request.data.get('name')

    if not name:
        return Response(
            {'error': 'name is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if Genre.objects.filter(name__iexact=name).exists():
        return Response(
            {'error': 'A genre with this name already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    genre = Genre.objects.create(name=name)

    return Response({
        'message': f'Genre "{genre.name}" created successfully',
        'genre': GenreSerializer(genre).data
    }, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_genre(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    genre_id = request.data.get('genre_id')

    if not genre_id:
        return Response(
            {'error': 'genre_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        genre = Genre.objects.get(id=genre_id)
    except Genre.DoesNotExist:
        return Response(
            {'error': 'Genre not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    name = request.data.get('name')
    is_active = request.data.get('is_active')

    if name is not None:
        if Genre.objects.filter(name__iexact=name).exclude(id=genre_id).exists():
            return Response(
                {'error': 'A genre with this name already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        genre.name = name

    if is_active is not None:
        genre.is_active = is_active

    genre.save()

    return Response({
        'message': f'Genre "{genre.name}" updated successfully',
        'genre': GenreSerializer(genre).data
    })


# ─── Content Rating ───────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_content_ratings(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    is_active = request.query_params.get('is_active')
    ratings = ContentRating.objects.all().order_by('code')

    if is_active is not None:
        ratings = ratings.filter(is_active=is_active.lower() == 'true')

    return Response({
        'count': ratings.count(),
        'content_ratings': ContentRatingSerializer(ratings, many=True).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_content_rating(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    code = request.data.get('code')
    name = request.data.get('name')
    description = request.data.get('description')

    if not code or not name or not description:
        return Response(
            {'error': 'code, name and description are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if ContentRating.objects.filter(code__iexact=code).exists():
        return Response(
            {'error': 'A content rating with this code already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    rating = ContentRating.objects.create(
        code=code.upper(),
        name=name,
        description=description
    )

    return Response({
        'message': f'Content rating "{rating.name}" created successfully',
        'content_rating': ContentRatingSerializer(rating).data
    }, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_content_rating(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    rating_id = request.data.get('rating_id')

    if not rating_id:
        return Response(
            {'error': 'rating_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        rating = ContentRating.objects.get(id=rating_id)
    except ContentRating.DoesNotExist:
        return Response(
            {'error': 'Content rating not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    code = request.data.get('code')
    name = request.data.get('name')
    description = request.data.get('description')
    is_active = request.data.get('is_active')

    if code is not None:
        if ContentRating.objects.filter(code__iexact=code).exclude(id=rating_id).exists():
            return Response(
                {'error': 'A content rating with this code already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        rating.code = code.upper()

    if name is not None:
        rating.name = name

    if description is not None:
        rating.description = description

    if is_active is not None:
        rating.is_active = is_active

    rating.save()

    return Response({
        'message': f'Content rating "{rating.name}" updated successfully',
        'content_rating': ContentRatingSerializer(rating).data
    })


# ─── Relationship Tag ─────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_relationship_tags(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    is_active = request.query_params.get('is_active')
    tags = RelationshipTag.objects.all().order_by('name')

    if is_active is not None:
        tags = tags.filter(is_active=is_active.lower() == 'true')

    return Response({
        'count': tags.count(),
        'relationship_tags': RelationshipTagSerializer(tags, many=True).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_relationship_tag(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    code = request.data.get('code')
    name = request.data.get('name')

    if not code or not name:
        return Response(
            {'error': 'code and name are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if RelationshipTag.objects.filter(code__iexact=code).exists():
        return Response(
            {'error': 'A relationship tag with this code already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    tag = RelationshipTag.objects.create(
        code=code.upper(),
        name=name
    )

    return Response({
        'message': f'Relationship tag "{tag.name}" created successfully',
        'relationship_tag': RelationshipTagSerializer(tag).data
    }, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_relationship_tag(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    tag_id = request.data.get('tag_id')

    if not tag_id:
        return Response(
            {'error': 'tag_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        tag = RelationshipTag.objects.get(id=tag_id)
    except RelationshipTag.DoesNotExist:
        return Response(
            {'error': 'Relationship tag not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    code = request.data.get('code')
    name = request.data.get('name')
    is_active = request.data.get('is_active')

    if code is not None:
        if RelationshipTag.objects.filter(code__iexact=code).exclude(id=tag_id).exists():
            return Response(
                {'error': 'A relationship tag with this code already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        tag.code = code.upper()

    if name is not None:
        tag.name = name

    if is_active is not None:
        tag.is_active = is_active

    tag.save()

    return Response({
        'message': f'Relationship tag "{tag.name}" updated successfully',
        'relationship_tag': RelationshipTagSerializer(tag).data
    })


# ─── Keyword ──────────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_keywords(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    is_active = request.query_params.get('is_active')
    keywords = Keyword.objects.all().order_by('name')

    if is_active is not None:
        keywords = keywords.filter(is_active=is_active.lower() == 'true')

    return Response({
        'count': keywords.count(),
        'keywords': KeywordSerializer(keywords, many=True).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_keyword(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    name = request.data.get('name')

    if not name:
        return Response(
            {'error': 'name is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if Keyword.objects.filter(name__iexact=name).exists():
        return Response(
            {'error': 'A keyword with this name already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    keyword = Keyword.objects.create(name=name)

    return Response({
        'message': f'Keyword "{keyword.name}" created successfully',
        'keyword': KeywordSerializer(keyword).data
    }, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_keyword(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    keyword_id = request.data.get('keyword_id')

    if not keyword_id:
        return Response(
            {'error': 'keyword_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        keyword = Keyword.objects.get(id=keyword_id)
    except Keyword.DoesNotExist:
        return Response(
            {'error': 'Keyword not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    name = request.data.get('name')
    is_active = request.data.get('is_active')

    if name is not None:
        if Keyword.objects.filter(name__iexact=name).exclude(id=keyword_id).exists():
            return Response(
                {'error': 'A keyword with this name already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        keyword.name = name

    if is_active is not None:
        keyword.is_active = is_active

    keyword.save()

    return Response({
        'message': f'Keyword "{keyword.name}" updated successfully',
        'keyword': KeywordSerializer(keyword).data
    })