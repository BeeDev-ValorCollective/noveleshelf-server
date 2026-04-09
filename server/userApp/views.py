from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from .serializers import RegisterSerializer, UserSerializer, UserProfileSerializer, AdminProfileSerializer, AuthorProfileSerializer
from .models import UserProfile, AdminProfile, AuthorProfile

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