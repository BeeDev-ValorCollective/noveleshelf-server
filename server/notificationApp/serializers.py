from rest_framework import serializers
from .models import NotificationType, NotificationPreference, NotificationPermission, SystemNotificationEmail, Notification


class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = ['id', 'code', 'label', 'description', 'recipient_type', 'sends_to_user', 'sends_to_admins', 'is_active']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    notification_type = NotificationTypeSerializer(read_only=True)

    class Meta:
        model = NotificationPreference
        fields = ['id', 'notification_type', 'is_enabled', 'updated_at']


class NotificationPermissionSerializer(serializers.ModelSerializer):
    notification_type = NotificationTypeSerializer(read_only=True)

    class Meta:
        model = NotificationPermission
        fields = ['id', 'notification_type', 'is_allowed', 'granted_by', 'updated_at']


class SystemNotificationEmailSerializer(serializers.ModelSerializer):
    notification_types = NotificationTypeSerializer(many=True, read_only=True)

    class Meta:
        model = SystemNotificationEmail
        fields = ['id', 'email', 'label', 'is_active', 'notification_types', 'created_at', 'updated_at']


class NotificationSerializer(serializers.ModelSerializer):
    notification_type = NotificationTypeSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'message', 'is_read', 'created_at']


class NotificationAdminSerializer(serializers.ModelSerializer):
    notification_type = NotificationTypeSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'notification_type', 'message', 'is_read', 'created_at']