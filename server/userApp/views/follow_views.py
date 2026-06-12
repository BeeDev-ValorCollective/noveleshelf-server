from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from userApp.models import UserFollowAuthor, AuthorProfile, FreeAuthorProfile


def _build_author_entry(follow):
    """Build a consistent author dict regardless of profile type."""
    if follow.author_profile:
        p = follow.author_profile
        return {
            'follow_id': follow.id,
            'profile_type': 'author',
            'profile_id': p.id,
            'author_username': p.author_username,
            'pen_name': p.pen_name,
            'avatar_url': p.avatar_url.url if p.avatar_url else None,
            'bio': p.bio,
            'is_featured': p.is_featured,
            'followed_at': follow.followed_at,
        }
    p = follow.free_author_profile
    return {
        'follow_id': follow.id,
        'profile_type': 'free_author',
        'profile_id': p.id,
        'author_username': p.author_username,
        'pen_name': p.pen_name,
        'avatar_url': p.avatar_url.url if p.avatar_url else None,
        'bio': p.bio,
        'is_featured': p.is_featured,
        'followed_at': follow.followed_at,
    }


class MyFollowingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List all authors the reader is following."""
        follows = (
            UserFollowAuthor.objects
            .filter(user=request.user)
            .select_related('author_profile', 'free_author_profile')
            .order_by('-followed_at')
        )
        return Response([_build_author_entry(f) for f in follows])

    def post(self, request):
        """
        Follow an author.
        Send either { "author_profile_id": 3 } or { "free_author_profile_id": 7 }
        """
        author_profile_id = request.data.get('author_profile_id')
        free_author_profile_id = request.data.get('free_author_profile_id')

        if not author_profile_id and not free_author_profile_id:
            return Response(
                {'detail': 'Provide either author_profile_id or free_author_profile_id.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if author_profile_id and free_author_profile_id:
            return Response(
                {'detail': 'Provide only one of author_profile_id or free_author_profile_id.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if author_profile_id:
            author = get_object_or_404(AuthorProfile, id=author_profile_id, is_publicly_visible=True, is_active=True)
            follow, created = UserFollowAuthor.objects.get_or_create(
                user=request.user, author_profile=author
            )
        else:
            author = get_object_or_404(FreeAuthorProfile, id=free_author_profile_id, is_publicly_visible=True, is_active=True)
            follow, created = UserFollowAuthor.objects.get_or_create(
                user=request.user, free_author_profile=author
            )

        if not created:
            return Response({'detail': 'Already following this author.'}, status=status.HTTP_200_OK)

        return Response(_build_author_entry(follow), status=status.HTTP_201_CREATED)


class UnfollowView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, follow_id):
        """Unfollow by the UserFollowAuthor record id."""
        follow = get_object_or_404(UserFollowAuthor, id=follow_id, user=request.user)
        follow.delete()
        return Response({'detail': 'Unfollowed.'}, status=status.HTTP_204_NO_CONTENT)