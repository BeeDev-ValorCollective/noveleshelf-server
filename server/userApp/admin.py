from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import User, UserProfile, UserWallet, AdminProfile, AuthorProfile, FreeAuthorProfile, ModeratorProfile, AuthorRequest, EmailVerificationToken

User = get_user_model()


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class UserWalletInline(admin.StackedInline):
    model = UserWallet
    can_delete = False


class AdminProfileInline(admin.StackedInline):
    model = AdminProfile
    can_delete = False


class AuthorProfileInline(admin.StackedInline):
    model = AuthorProfile
    can_delete = False


class FreeAuthorProfileInline(admin.StackedInline):
    model = FreeAuthorProfile
    can_delete = False


class ModeratorProfileInline(admin.StackedInline):
    model = ModeratorProfile
    can_delete = False
    fk_name = 'user'


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'date_of_birth', 'is_staff', 'is_superuser', 'default_login_role']
    inlines = [UserProfileInline, UserWalletInline, AdminProfileInline, AuthorProfileInline, FreeAuthorProfileInline, ModeratorProfileInline]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'default_login_role')}),
        ('Verification', {'fields': ('is_verified', 'verification_grace_ends')}),
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


class AuthorRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'request_type', 'status', 'contact_attempted', 'created_at', 'updated_at']
    list_filter = ['request_type', 'status', 'contact_attempted']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(UserWallet)
admin.site.register(AdminProfile)
admin.site.register(AuthorProfile)
admin.site.register(FreeAuthorProfile)
admin.site.register(ModeratorProfile)
admin.site.register(AuthorRequest, AuthorRequestAdmin)
admin.site.register(EmailVerificationToken)