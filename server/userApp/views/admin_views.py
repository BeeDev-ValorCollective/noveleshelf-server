from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from ..serializers import AdminProfileSerializer, AuthorProfileSerializer, ModeratorProfileSerializer
from ..models import AdminProfile, AuthorProfile, ModeratorProfile

User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upgrade_to_author(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if hasattr(user, 'author_profile'):
        return Response(
            {'error': 'User is already an author'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    show_real_name = request.data.get('show_real_name', False)

    AuthorProfile.objects.create(
        user=user,
        first_name=first_name,
        last_name=last_name,
        show_real_name=show_real_name
    )
    
    return Response({
        'message': f'{user.email} has been upgraded to author successfully',
        'author_profile': AuthorProfileSerializer(user.author_profile).data
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upgrade_to_admin(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if hasattr(user, 'admin_profile'):
        return Response(
            {'error': 'User is already an admin'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    AdminProfile.objects.create(
        user=user,
        admin_username=user.email,
        is_super_admin=False
    )
    
    user.is_staff = True
    user.save()
    
    return Response({
        'message': f'{user.email} has been upgraded to admin successfully',
        'admin_profile': AdminProfileSerializer(user.admin_profile).data
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upgrade_to_moderator(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if hasattr(user, 'moderator_profile'):
        return Response(
            {'error': 'User is already a moderator'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    ModeratorProfile.objects.create(
        user=user,
        assigned_by=request.user
    )
    
    return Response({
        'message': f'{user.email} has been upgraded to moderator successfully',
        'moderator_profile': ModeratorProfileSerializer(user.moderator_profile).data
    }, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def admin_update_author(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if not hasattr(user, 'author_profile'):
        return Response(
            {'error': 'User does not have an author profile'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    author_profile = user.author_profile
    
    tier = request.data.get('tier')
    contract_link = request.data.get('contract_link')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    show_real_name = request.data.get('show_real_name')

    if tier is not None:
        try:
            tier = int(tier)
            if tier < 1 or tier > 5:
                return Response(
                    {'error': 'Tier must be between 1 and 5'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            author_profile.tier = tier
        except ValueError:
            return Response(
                {'error': 'Tier must be a number'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    if contract_link is not None:
        author_profile.contract_link = contract_link

    if first_name is not None:
        author_profile.first_name = first_name

    if last_name is not None:
        author_profile.last_name = last_name

    if show_real_name is not None:
        author_profile.show_real_name = show_real_name
    
    author_profile.save()
    
    return Response({
        'message': f'{user.email} author profile updated successfully',
        'author_profile': AuthorProfileSerializer(author_profile).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deactivate_user(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if user == request.user:
        return Response(
            {'error': 'You cannot deactivate your own account'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.is_active = False
    user.save()
    
    return Response({
        'message': f'{user.email} has been deactivated successfully'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reactivate_user(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    user_id = request.data.get('user_id')
    
    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    user.is_active = True
    user.save()
    
    return Response({
        'message': f'{user.email} has been reactivated successfully'
    })