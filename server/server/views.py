from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from userApp.serializers import UserSerializer


@api_view(['GET'])
def health_check(request):
    return Response({"status": "ok", "message": "Django is talking!"})


@api_view(['POST'])
@permission_classes([AllowAny])
def debug_login(request):
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
        },
        'debug': {
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'has_admin_profile': hasattr(user, 'admin_profile'),
            'has_author_profile': hasattr(user, 'author_profile'),
            'has_moderator_profile': hasattr(user, 'moderator_profile'),
            'default_login_role': user.default_login_role,
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def debug_me(request):
    return Response({
        'user': UserSerializer(request.user).data,
        'debug': {
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
            'has_admin_profile': hasattr(request.user, 'admin_profile'),
            'has_author_profile': hasattr(request.user, 'author_profile'),
            'has_moderator_profile': hasattr(user, 'moderator_profile'),
            'default_login_role': request.user.default_login_role,
        }
    })