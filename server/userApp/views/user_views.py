from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.contrib.auth import get_user_model
from ..serializers import UserProfileSerializer, AdminProfileSerializer, AuthorProfileSerializer, ModeratorProfileSerializer, FreeAuthorProfileSerializer, AuthorRequestSerializer
from ..models import UserProfile, AdminProfile, AuthorProfile, ModeratorProfile, FreeAuthorProfile, AuthorRequest
from utils.email_utils import send_verification_email
from django.utils import timezone
from datetime import timedelta

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
    
    valid_roles = ['reader', 'author', 'moderator', 'admin', 'free_author']
    if role not in valid_roles:
        return Response(
            {'error': f'Invalid role. Must be one of: {", ".join(valid_roles)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if role == 'free_author' and not hasattr(request.user, 'free_author_profile'):
        return Response(
            {'error': 'You do not have a free author profile'},
            status=status.HTTP_403_FORBIDDEN
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if not current_password or not new_password or not confirm_password:
        return Response(
            {'error': 'Current password, new password and confirm password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not request.user.check_password(current_password):
        return Response(
            {'error': 'Current password is incorrect'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if new_password != confirm_password:
        return Response(
            {'error': 'New passwords do not match'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if len(new_password) < 8:
        return Response(
            {'error': 'New password must be at least 8 characters'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if current_password == new_password:
        return Response(
            {'error': 'New password must be different from current password'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # change password
    request.user.set_password(new_password)
    request.user.save()

    # blacklist all existing tokens
    try:
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
    except Exception as e:
        print(f'Token blacklist error: {e}')

    return Response({
        'message': 'Password changed successfully. Please log in again.'
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_email(request):
    new_email = request.data.get('new_email')
    password = request.data.get('password')

    if not new_email or not password:
        return Response(
            {'error': 'New email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not request.user.check_password(password):
        return Response(
            {'error': 'Password is incorrect'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if new_email == request.user.email:
        return Response(
            {'error': 'New email must be different from current email'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # check if email already in use
    if User.objects.filter(email=new_email).exists():
        return Response(
            {'error': 'Email already in use'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # update email and reset verification
    request.user.email = new_email
    request.user.is_verified = False
    request.user.verification_grace_ends = timezone.now() + timedelta(days=7)
    request.user.save()

    # blacklist all existing tokens
    try:
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
    except Exception as e:
        print(f'Token blacklist error: {e}')

    # send verification email to new address
    try:
        send_verification_email(request.user)
    except Exception as e:
        print(f'Verification email failed: {e}')

    return Response({
        'message': f'Email changed successfully. Please verify your new email address at {new_email}. You have been logged out.'
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upgrade_to_free_author(request):
    if not request.user.is_verified:
        return Response(
            {'error': 'Please verify your email before upgrading to a free author'},
            status=status.HTTP_403_FORBIDDEN
        )

    if hasattr(request.user, 'free_author_profile'):
        return Response(
            {'error': 'You already have a free author profile'},
            status=status.HTTP_400_BAD_REQUEST
        )

    is_paid_author = hasattr(request.user, 'author_profile')

    FreeAuthorProfile.objects.create(
        user=request.user,
        is_publicly_visible=True
    )

    if not is_paid_author:
        request.user.default_login_role = 'free_author'
        request.user.save()

    return Response({
        'message': 'You have been upgraded to free author successfully',
        'is_also_paid_author': is_paid_author,
        'free_author_profile': FreeAuthorProfileSerializer(request.user.free_author_profile).data
    }, status=status.HTTP_201_CREATED)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_free_author_profile(request):
    if not hasattr(request.user, 'free_author_profile'):
        return Response(
            {'error': 'Free author profile not found'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    free_author_profile = request.user.free_author_profile
    
    author_username = request.data.get('author_username')
    pen_name = request.data.get('pen_name')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    bio = request.data.get('bio')
    show_real_name = request.data.get('show_real_name')
    avatar = request.data.get('avatar_url')

    is_publicly_visible = request.data.get('is_publicly_visible')

    if is_publicly_visible is not None:
        free_author_profile.is_publicly_visible = is_publicly_visible

    if author_username:
        if FreeAuthorProfile.objects.filter(author_username=author_username).exclude(user=request.user).exists():
            return Response(
                {'error': 'Author username already taken'},
                status=status.HTTP_400_BAD_REQUEST
            )
        free_author_profile.author_username = author_username

    if pen_name is not None:
        free_author_profile.pen_name = pen_name

    if first_name is not None:
        free_author_profile.first_name = first_name

    if last_name is not None:
        free_author_profile.last_name = last_name

    if bio is not None:
        free_author_profile.bio = bio

    if show_real_name is not None:
        free_author_profile.show_real_name = show_real_name

    if avatar:
        free_author_profile.avatar_url = avatar

    free_author_profile.save()

    return Response({
        'message': 'Free author profile updated successfully',
        'free_author_profile': FreeAuthorProfileSerializer(free_author_profile).data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_author_request(request):
    if not request.user.is_verified:
        return Response(
            {'error': 'Please verify your email before submitting an author request'},
            status=status.HTTP_403_FORBIDDEN
        )

    request_type = request.data.get('request_type')

    if not request_type:
        return Response(
            {'error': 'request_type is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    valid_types = ['new_author', 'new_genre', 'tier_review', 'contract_addendum', 'leave_platform', 'rejoin_platform']
    if request_type not in valid_types:
        return Response(
            {'error': f'Invalid request type. Must be one of: {", ".join(valid_types)}'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # new_author requests only for non paid authors
    if request_type == 'new_author' and hasattr(request.user, 'author_profile'):
        return Response(
            {'error': 'You already have a paid author profile. Use author_change request types instead.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # non new_author requests only for paid authors
    if request_type != 'new_author' and not hasattr(request.user, 'author_profile'):
        return Response(
            {'error': 'You must be a paid author to submit this type of request'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # check for active requests
    active_statuses = ['pending', 'in_progress']
    existing_request = AuthorRequest.objects.filter(
        user=request.user,
        status__in=active_statuses
    ).first()

    if existing_request:
        return Response(
            {'error': 'You already have an active request. Please wait for it to be resolved before submitting a new one.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    bio = request.data.get('bio')
    genre_interest = request.data.get('genre_interest')
    writing_sample_link = request.data.get('writing_sample_link')

    author_request = AuthorRequest.objects.create(
        user=request.user,
        request_type=request_type,
        bio=bio,
        genre_interest=genre_interest,
        writing_sample_link=writing_sample_link
    )

    return Response({
        'message': 'Your request has been submitted successfully. We will be in touch.',
        'request': AuthorRequestSerializer(author_request).data
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_author_requests(request):
    requests = AuthorRequest.objects.filter(user=request.user).order_by('-created_at')
    
    return Response({
        'count': requests.count(),
        'requests': AuthorRequestSerializer(requests, many=True).data
    })