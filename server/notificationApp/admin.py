from django.contrib import admin
from .models import NotificationType, NotificationPreference, NotificationPermission, SystemNotificationEmail, Notification


class NotificationPreferenceInline(admin.TabularInline):
    model = NotificationPreference
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


class NotificationPermissionInline(admin.TabularInline):
    model = NotificationPermission
    extra = 0
    readonly_fields = ['created_at', 'updated_at']


class SystemNotificationEmailAdmin(admin.ModelAdmin):
    list_display = ['label', 'email', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['email', 'label']
    filter_horizontal = ['notification_types']
    readonly_fields = ['created_at', 'updated_at']


class NotificationTypeAdmin(admin.ModelAdmin):
    list_display = ['label', 'code', 'recipient_type', 'sends_to_user', 'sends_to_admins', 'is_active']
    list_filter = ['recipient_type', 'is_active']
    search_fields = ['label', 'code']
    readonly_fields = ['created_at']


class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'is_enabled', 'created_at']
    list_filter = ['is_enabled', 'notification_type']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']


class NotificationPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'granted_by', 'is_allowed', 'created_at']
    list_filter = ['is_allowed', 'notification_type']
    search_fields = ['user__email', 'granted_by__email']
    readonly_fields = ['created_at', 'updated_at']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['is_read', 'notification_type']
    search_fields = ['user__email']
    readonly_fields = ['created_at']

    def has_add_permission(self, request):
        return False


admin.site.register(NotificationType, NotificationTypeAdmin)
admin.site.register(NotificationPreference, NotificationPreferenceAdmin)
admin.site.register(NotificationPermission, NotificationPermissionAdmin)
admin.site.register(SystemNotificationEmail, SystemNotificationEmailAdmin)
admin.site.register(Notification, NotificationAdmin)