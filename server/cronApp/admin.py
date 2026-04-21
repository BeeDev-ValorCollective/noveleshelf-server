from django.contrib import admin
from .models import CronLog


class CronLogAdmin(admin.ModelAdmin):
    list_display = ['job_name', 'status', 'records_affected', 'message', 'created_at']
    list_filter = ['job_name', 'status']
    readonly_fields = ['job_name', 'status', 'message', 'records_affected', 'created_at']
    ordering = ['-created_at']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(CronLog, CronLogAdmin)