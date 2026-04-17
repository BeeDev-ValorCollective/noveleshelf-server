from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from ..serializers import RegisterSerializer, UserSerializer
from utils.email_utils import send_verification_email
from userApp.models import EmailVerificationToken
from django.utils import timezone
from ..models import EmailVerificationToken

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        try:
            send_verification_email(user)
        except Exception as e:
            print(f'Verification email failed: {e}')

        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            'message': 'Account created. Please check your email to verify your account.'
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

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request):
    token = request.query_params.get('token')
    
    if not token:
        return Response(
            {'error': 'Token is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        verification_token = EmailVerificationToken.objects.get(
            token=token,
            is_used=False
        )
    except EmailVerificationToken.DoesNotExist:
        return Response(
            {'error': 'Invalid or expired token'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if verification_token.expires_at < timezone.now():
        return Response(
            {'error': 'Token has expired. Please request a new verification email.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = verification_token.user
    user.is_verified = True
    user.save()
    
    verification_token.is_used = True
    verification_token.save()
    
    return Response({
        'message': 'Email verified successfully. You now have full access to NovelShelf.'
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def resend_verification(request):
    if request.user.is_verified:
        return Response(
            {'error': 'Your email is already verified'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    EmailVerificationToken.objects.filter(
        user=request.user,
        is_used=False
    ).update(is_used=True)
    
    try:
        send_verification_email(request.user)
        return Response({
            'message': 'Verification email sent. Please check your inbox.'
        })
    except Exception as e:
        return Response(
            {'error': 'Failed to send verification email. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )