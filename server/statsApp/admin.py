# statsApp/admin.py
from django.contrib import admin
from .models import DailyActivity, Event


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'platform', 'date', 'occurrence_count', 'updated_at']
    list_filter = ['activity_type', 'platform', 'date']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['user', 'event_type', 'platform', 'created_at']
    list_filter = ['event_type', 'platform', 'created_at']
    search_fields = ['user__email', 'event_type']
    readonly_fields = ['user', 'event_type', 'platform', 'metadata', 'created_at']

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser