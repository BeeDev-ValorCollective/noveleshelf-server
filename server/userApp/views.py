from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from .serializers import RegisterSerializer, UserSerializer, UserProfileSerializer, AdminProfileSerializer, AuthorProfileSerializer, ModeratorProfileSerializer
from .models import UserProfile, AdminProfile, AuthorProfile, ModeratorProfile

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Email and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, username=email, password=password)

    if not user:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    refresh = RefreshToken.for_user(user)
    return Response({
        'user': UserSerializer(user).data,
        'tokens': {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except Exception:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upgrade_to_author(request):
    if not hasattr(request.user, 'admin_profile'):
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
    
    AuthorProfile.objects.create(user=user)
    
    return Response({
        'message': f'{user.email} has been upgraded to author successfully',
        'author_profile': AuthorProfileSerializer(user.author_profile).data
    }, status=status.HTTP_201_CREATED)

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
    
    if author_username:
        if AuthorProfile.objects.filter(author_username=author_username).exclude(user=request.user).exists():
            return Response(
                {'error': 'Author username already taken'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author_profile.author_username = author_username
    
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
def admin_update_author(request):
    if not hasattr(request.user, 'admin_profile'):
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
    
    author_profile.save()
    
    return Response({
        'message': f'{user.email} author profile updated successfully',
        'author_profile': AuthorProfileSerializer(author_profile).data
    })

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
    
    # make sure user actually has the profile for the role they are setting
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