from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import User, UserProfile, UserWallet, AdminProfile

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'date_of_birth', 'is_staff', 'is_superuser']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'date_of_birth'),
        }),
    )
    
    search_fields = ['email']
    filter_horizontal = ('groups', 'user_permissions',)

# admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(UserWallet)
admin.site.register(AdminProfile)