from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from django.contrib.auth import get_user_model
from ..serializers import RegisterSerializer, UserSerializer
from utils.email_utils import send_verification_email, send_password_reset_email
from userApp.models import EmailVerificationToken, PasswordResetToken
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
            'message': f'Account created. Please check {user.email} to verify your account.'
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

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.check_password(password):
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_active:
        if not user.is_verified:
            return Response(
                {'error': 'Your account has been deactivated due to unverified email. Please use the resend verification option to reactivate your account.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {'error': 'Your account has been deactivated. Please contact support.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_verified:
        days_left = (user.verification_grace_ends - timezone.now()).days
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            'warning': f'Please verify your email. Your account will be deactivated in {days_left} days if not verified.'
        })

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
            'message': f'Verification email sent to {request.user.email}. Please check your inbox.'
        })
    except Exception as e:
        return Response(
            {'error': 'Failed to send verification email. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')

    if not email:
        return Response(
            {'error': 'Email is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # don't reveal if email exists or not for security
        return Response({
            'message': 'If an account exists with that email you will receive a password reset link shortly.'
        })

    # check if email is verified
    if not user.is_verified:
        return Response(
            {'error': 'Your email address is not verified. Please verify your email before resetting your password.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # invalidate any existing unused reset tokens
    PasswordResetToken.objects.filter(
        user=user,
        is_used=False
    ).update(is_used=True)

    try:
        send_password_reset_email(user)
    except Exception as e:
        print(f'Password reset email failed: {e}')
        return Response(
            {'error': 'Failed to send reset email. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return Response({
        'message': 'If an account exists with that email you will receive a password reset link shortly.'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    token = request.data.get('token')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if not token or not new_password or not confirm_password:
        return Response(
            {'error': 'Token, new password and confirm password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if new_password != confirm_password:
        return Response(
            {'error': 'Passwords do not match'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if len(new_password) < 8:
        return Response(
            {'error': 'Password must be at least 8 characters'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        reset_token = PasswordResetToken.objects.get(
            token=token,
            is_used=False
        )
    except PasswordResetToken.DoesNotExist:
        return Response(
            {'error': 'Invalid or expired reset token'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if reset_token.expires_at < timezone.now():
        return Response(
            {'error': 'Reset token has expired. Please request a new password reset.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = reset_token.user

    # set new password
    user.set_password(new_password)
    user.save()

    # mark token as used
    reset_token.is_used = True
    reset_token.save()

    # blacklist all existing tokens
    try:
        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)
    except Exception as e:
        print(f'Token blacklist error: {e}')

    return Response({
        'message': 'Password reset successfully. Please log in with your new password.'
    })