# statsApp/admin.py
from django.contrib import admin
from .models import DailyActivity, Event


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'platform', 'date', 'occurrence_count', 'updated_at']
    list_filter = ['activity_type', 'platform', 'date']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']

    # View access is controlled entirely through Django's Group permissions
    # (grant "Can view daily activity" to whichever staff group should see it).
    # Superusers see it automatically since they bypass all permission checks.
    # Add/change/delete stay locked for everyone — this is a read-only log.
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['user', 'event_type', 'platform', 'created_at']
    list_filter = ['event_type', 'platform', 'created_at']
    search_fields = ['user__email', 'event_type']
    readonly_fields = ['user', 'event_type', 'platform', 'metadata', 'created_at']

    # Same pattern as DailyActivityAdmin — group-controlled view access,
    # add/change/delete always locked regardless of group permissions.
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False