from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from ..serializers import UserProfileSerializer, AdminProfileSerializer, AuthorProfileSerializer, ModeratorProfileSerializer
from ..models import UserProfile, AdminProfile, AuthorProfile, ModeratorProfile

User = get_user_model()


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_profile(request):
    profile = request.user.profile
    
    username = request.data.get('username')
    bio = request.data.get('bio')
    avatar = request.data.get('avatar_url')
    
    if username:
        if UserProfile.objects.filter(username=username).exclude(user=request.user).exists():
            return Response(
                {'error': 'Username already taken'},
                status=status.HTTP_400_BAD_REQUEST
            )
        profile.username = username
    
    if bio is not None:
        profile.bio = bio
    
    if avatar:
        profile.avatar_url = avatar
    
    profile.save()
    
    return Response({
        'message': 'Profile updated successfully',
        'profile': UserProfileSerializer(profile).data
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_admin_profile(request):
    if not hasattr(request.user, 'admin_profile'):
        return Response(
            {'error': 'Admin profile not found'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    admin_profile = request.user.admin_profile
    
    admin_username = request.data.get('admin_username')
    avatar = request.data.get('avatar_url')
    
    if admin_username:
        if AdminProfile.objects.filter(admin_username=admin_username).exclude(user=request.user).exists():
            return Response(
                {'error': 'Admin username already taken'},
                status=status.HTTP_400_BAD_REQUEST
            )
        admin_profile.admin_username = admin_username
    
    if avatar:
        admin_profile.avatar_url = avatar
    
    admin_profile.save()
    
    return Response({
        'message': 'Admin profile updated successfully',
        'admin_profile': AdminProfileSerializer(admin_profile).data
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_author_profile(request):
    if not hasattr(request.user, 'author_profile'):
        return Response(
            {'error': 'Author profile not found'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    author_profile = request.user.author_profile
    
    author_username = request.data.get('author_username')
    pen_name = request.data.get('pen_name')
    bio = request.data.get('bio')
    avatar = request.data.get('avatar_url')
    show_real_name = request.data.get('show_real_name')
    
    if author_username:
        if AuthorProfile.objects.filter(author_username=author_username).exclude(user=request.user).exists():
            return Response(
                {'error': 'Author username already taken'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author_profile.author_username = author_username
    
    if show_real_name is not None:
        author_profile.show_real_name = show_real_name
    
    if pen_name is not None:
        author_profile.pen_name = pen_name
    
    if bio is not None:
        author_profile.bio = bio
    
    if avatar:
        author_profile.avatar_url = avatar
    
    author_profile.save()
    
    return Response({
        'message': 'Author profile updated successfully',
        'author_profile': AuthorProfileSerializer(author_profile).data
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_moderator_profile(request):
    if not hasattr(request.user, 'moderator_profile'):
        return Response(
            {'error': 'Moderator profile not found'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    moderator_profile = request.user.moderator_profile
    
    mod_username = request.data.get('mod_username')
    avatar = request.data.get('avatar_url')
    
    if mod_username:
        if ModeratorProfile.objects.filter(mod_username=mod_username).exclude(user=request.user).exists():
            return Response(
                {'error': 'Moderator username already taken'},
                status=status.HTTP_400_BAD_REQUEST
            )
        moderator_profile.mod_username = mod_username
    
    if avatar:
        moderator_profile.avatar_url = avatar
    
    moderator_profile.save()
    
    return Response({
        'message': 'Moderator profile updated successfully',
        'moderator_profile': ModeratorProfileSerializer(moderator_profile).data
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_default_role(request):
    role = request.data.get('default_login_role')
    
    if not role:
        return Response(
            {'error': 'default_login_role is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    valid_roles = ['reader', 'author', 'moderator', 'admin']
    if role not in valid_roles:
        return Response(
            {'error': f'Invalid role. Must be one of: {", ".join(valid_roles)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if role == 'author' and not hasattr(request.user, 'author_profile'):
        return Response(
            {'error': 'You do not have an author profile'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if role == 'moderator' and not hasattr(request.user, 'moderator_profile'):
        return Response(
            {'error': 'You do not have a moderator profile'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if role == 'admin' and not hasattr(request.user, 'admin_profile'):
        return Response(
            {'error': 'You do not have an admin profile'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    request.user.default_login_role = role
    request.user.save()
    
    return Response({
        'message': f'Default login role updated to {role}',
        'default_login_role': request.user.default_login_role
    })