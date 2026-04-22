from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from ..serializers import AdminProfileSerializer, AuthorProfileSerializer, ModeratorProfileSerializer, UserSerializer, FreeAuthorProfileSerializer, AuthorRequestAdminSerializer, AuthorRequestSerializer
from ..models import AdminProfile, AuthorProfile, ModeratorProfile, FreeAuthorProfile, AuthorRequest
from utils.email_utils import send_author_approved_email

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
    is_publicly_visible = request.data.get('is_publicly_visible')

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
    
    if is_publicly_visible is not None:
        author_profile.is_publicly_visible = is_publicly_visible
    
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

from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    role = request.query_params.get('role')
    is_active = request.query_params.get('is_active')
    
    users = User.objects.all()
    
    if role == 'author':
        users = users.filter(author_profile__isnull=False)
    elif role == 'admin':
        users = users.filter(admin_profile__isnull=False)
    elif role == 'moderator':
        users = users.filter(moderator_profile__isnull=False)
    elif role == 'reader':
        users = users.filter(
            author_profile__isnull=True,
            admin_profile__isnull=True,
            moderator_profile__isnull=True
        )
    
    if is_active is not None:
        is_active_bool = is_active.lower() == 'true'
        users = users.filter(is_active=is_active_bool)
    
    # pagination
    page_size = 20
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size
    
    total = users.count()
    users_page = users[start:end]
    
    return Response({
        'count': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size,
        'next': f'?page={page + 1}' if end < total else None,
        'previous': f'?page={page - 1}' if page > 1 else None,
        'results': UserSerializer(users_page, many=True).data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_author_requests(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    status_filter = request.query_params.get('status')
    request_type = request.query_params.get('request_type')
    contact_attempted = request.query_params.get('contact_attempted')

    requests = AuthorRequest.objects.all().order_by('-created_at')

    if status_filter:
        requests = requests.filter(status=status_filter)

    if request_type:
        requests = requests.filter(request_type=request_type)

    if contact_attempted is not None:
        contact_attempted_bool = contact_attempted.lower() == 'true'
        requests = requests.filter(contact_attempted=contact_attempted_bool)

    # pagination
    page_size = 20
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size

    total = requests.count()
    requests_page = requests[start:end]

    return Response({
        'count': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size,
        'next': f'?page={page + 1}' if end < total else None,
        'previous': f'?page={page - 1}' if page > 1 else None,
        'results': AuthorRequestAdminSerializer(requests_page, many=True).data
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_author_request(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    request_id = request.data.get('request_id')

    if not request_id:
        return Response(
            {'error': 'request_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        author_request = AuthorRequest.objects.get(id=request_id)
    except AuthorRequest.DoesNotExist:
        return Response(
            {'error': 'Request not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    status_value = request.data.get('status')
    admin_notes = request.data.get('admin_notes')
    reader_notes = request.data.get('reader_notes')
    contact_attempted = request.data.get('contact_attempted')

    valid_statuses = ['pending', 'in_progress', 'approved', 'not_at_this_time', 'cleared']

    if status_value:
        if status_value not in valid_statuses:
            return Response(
                {'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # approved status should use approve_author_request endpoint
        if status_value == 'approved':
            return Response(
                {'error': 'Use the approve-author-request endpoint to approve requests'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author_request.status = status_value

    if admin_notes is not None:
        author_request.admin_notes = admin_notes

    if reader_notes is not None:
        author_request.reader_notes = reader_notes

    if contact_attempted is not None:
        author_request.contact_attempted = contact_attempted

    author_request.save()

    return Response({
        'message': 'Request updated successfully',
        'request': AuthorRequestAdminSerializer(author_request).data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_author_request(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    request_id = request.data.get('request_id')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not request_id:
        return Response(
            {'error': 'request_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        author_request = AuthorRequest.objects.get(id=request_id)
    except AuthorRequest.DoesNotExist:
        return Response(
            {'error': 'Request not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    if author_request.status == 'approved':
        return Response(
            {'error': 'This request has already been approved'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = author_request.user

    # handle based on request type
    if author_request.request_type == 'new_author':
        if hasattr(user, 'author_profile'):
            return Response(
                {'error': 'User already has a paid author profile'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not first_name or not last_name:
            return Response(
                {'error': 'first_name and last_name are required to approve a new author request'},
                status=status.HTTP_400_BAD_REQUEST
            )

        AuthorProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
        )

    elif author_request.request_type == 'leave_platform':
        if hasattr(user, 'author_profile'):
            user.author_profile.is_active = False
            user.author_profile.is_publicly_visible = False
            user.author_profile.save()

    elif author_request.request_type == 'rejoin_platform':
        if hasattr(user, 'author_profile'):
            user.author_profile.is_active = True
            user.author_profile.save()

    # mark request as approved
    author_request.status = 'approved'
    author_request.save()

    # send approval email
    try:
        send_author_approved_email(user, author_request.request_type)
    except Exception as e:
        print(f'Author approved email failed: {e}')

    return Response({
        'message': f'{user.email} request has been approved successfully',
        'request': AuthorRequestAdminSerializer(author_request).data
    }, status=status.HTTP_200_OK)