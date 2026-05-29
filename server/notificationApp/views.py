from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import NotificationType, NotificationPreference, NotificationPermission, SystemNotificationEmail, Notification
from .serializers import (
    NotificationTypeSerializer,
    NotificationPreferenceSerializer,
    NotificationPermissionSerializer,
    SystemNotificationEmailSerializer,
    NotificationSerializer,
    NotificationAdminSerializer
)


# ─── User endpoints ───────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    unread_count = notifications.filter(is_read=False).count()

    page_size = 20
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size
    total = notifications.count()

    return Response({
        'unread_count': unread_count,
        'count': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size,
        'next': f'?page={page + 1}' if end < total else None,
        'previous': f'?page={page - 1}' if page > 1 else None,
        'results': NotificationSerializer(notifications[start:end], many=True).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request):
    notification_id = request.data.get('notification_id')

    if not notification_id:
        return Response(
            {'error': 'notification_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        notification = Notification.objects.get(
            id=notification_id,
            user=request.user
        )
    except Notification.DoesNotExist:
        return Response(
            {'error': 'Notification not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    notification.is_read = True
    notification.save()

    return Response({
        'message': 'Notification marked as read'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_read(request):
    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)

    return Response({
        'message': 'All notifications marked as read'
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_notifications(request):
    Notification.objects.filter(user=request.user).delete()

    return Response({
        'message': 'All notifications cleared'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_preferences(request):
    # get all active notification types
    notification_types = NotificationType.objects.filter(is_active=True)

    # get user's existing preferences
    preferences = NotificationPreference.objects.filter(user=request.user)
    preferences_map = {p.notification_type_id: p for p in preferences}

    # get what the user is allowed to toggle
    permissions = NotificationPermission.objects.filter(user=request.user)
    permissions_map = {p.notification_type_id: p for p in permissions}

    result = []
    for nt in notification_types:
        # skip if user doesn't have permission to see this type
        permission = permissions_map.get(nt.id)
        if permission and not permission.is_allowed:
            continue

        preference = preferences_map.get(nt.id)
        result.append({
            'notification_type': NotificationTypeSerializer(nt).data,
            'is_enabled': preference.is_enabled if preference else True,
            'can_toggle': True
        })

    return Response({
        'count': len(result),
        'preferences': result
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_my_preference(request):
    notification_type_id = request.data.get('notification_type_id')
    is_enabled = request.data.get('is_enabled')

    if not notification_type_id or is_enabled is None:
        return Response(
            {'error': 'notification_type_id and is_enabled are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # check permission
    permission = NotificationPermission.objects.filter(
        user=request.user,
        notification_type_id=notification_type_id
    ).first()

    if permission and not permission.is_allowed:
        return Response(
            {'error': 'You do not have permission to toggle this notification'},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        notification_type = NotificationType.objects.get(id=notification_type_id, is_active=True)
    except NotificationType.DoesNotExist:
        return Response(
            {'error': 'Notification type not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    preference, created = NotificationPreference.objects.get_or_create(
        user=request.user,
        notification_type=notification_type,
        defaults={'is_enabled': is_enabled}
    )

    if not created:
        preference.is_enabled = is_enabled
        preference.save()

    return Response({
        'message': f'Notification preference updated',
        'notification_type': NotificationTypeSerializer(notification_type).data,
        'is_enabled': preference.is_enabled
    })


# ─── Admin endpoints ───────────────────────────────────────────

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notification_types(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    notification_types = NotificationType.objects.all()
    return Response({
        'count': notification_types.count(),
        'results': NotificationTypeSerializer(notification_types, many=True).data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_preferences(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response(
            {'error': 'user_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    preferences = NotificationPreference.objects.filter(user_id=user_id)
    return Response({
        'count': preferences.count(),
        'preferences': NotificationPreferenceSerializer(preferences, many=True).data
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user_preference(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    user_id = request.data.get('user_id')
    notification_type_id = request.data.get('notification_type_id')
    is_enabled = request.data.get('is_enabled')

    if not user_id or not notification_type_id or is_enabled is None:
        return Response(
            {'error': 'user_id, notification_type_id and is_enabled are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        notification_type = NotificationType.objects.get(id=notification_type_id)
    except NotificationType.DoesNotExist:
        return Response(
            {'error': 'Notification type not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    preference, created = NotificationPreference.objects.get_or_create(
        user_id=user_id,
        notification_type=notification_type,
        defaults={'is_enabled': is_enabled}
    )

    if not created:
        preference.is_enabled = is_enabled
        preference.save()

    return Response({
        'message': 'User preference updated',
        'preference': NotificationPreferenceSerializer(preference).data
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user_permission(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    user_id = request.data.get('user_id')
    notification_type_id = request.data.get('notification_type_id')
    is_allowed = request.data.get('is_allowed')

    if not user_id or not notification_type_id or is_allowed is None:
        return Response(
            {'error': 'user_id, notification_type_id and is_allowed are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        notification_type = NotificationType.objects.get(id=notification_type_id)
    except NotificationType.DoesNotExist:
        return Response(
            {'error': 'Notification type not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    permission, created = NotificationPermission.objects.get_or_create(
        user_id=user_id,
        notification_type=notification_type,
        defaults={
            'granted_by': request.user,
            'is_allowed': is_allowed
        }
    )

    if not created:
        permission.is_allowed = is_allowed
        permission.save()

    return Response({
        'message': 'User permission updated',
        'permission': NotificationPermissionSerializer(permission).data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_system_emails(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    emails = SystemNotificationEmail.objects.all()
    return Response({
        'count': emails.count(),
        'results': SystemNotificationEmailSerializer(emails, many=True).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_system_email(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    email = request.data.get('email')
    label = request.data.get('label')
    notification_type_ids = request.data.get('notification_type_ids', [])

    if not email or not label:
        return Response(
            {'error': 'email and label are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if SystemNotificationEmail.objects.filter(email=email).exists():
        return Response(
            {'error': 'This email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    system_email = SystemNotificationEmail.objects.create(
        email=email,
        label=label,
        created_by=request.user
    )

    if notification_type_ids:
        system_email.notification_types.set(notification_type_ids)

    return Response({
        'message': 'System notification email created',
        'system_email': SystemNotificationEmailSerializer(system_email).data
    }, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_system_email(request):
    if not request.user.is_staff:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )

    system_email_id = request.data.get('system_email_id')
    if not system_email_id:
        return Response(
            {'error': 'system_email_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        system_email = SystemNotificationEmail.objects.get(id=system_email_id)
    except SystemNotificationEmail.DoesNotExist:
        return Response(
            {'error': 'System email not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    label = request.data.get('label')
    is_active = request.data.get('is_active')
    notification_type_ids = request.data.get('notification_type_ids')

    if label is not None:
        system_email.label = label
    if is_active is not None:
        system_email.is_active = is_active
    if notification_type_ids is not None:
        system_email.notification_types.set(notification_type_ids)

    system_email.save()

    return Response({
        'message': 'System email updated',
        'system_email': SystemNotificationEmailSerializer(system_email).data
    })