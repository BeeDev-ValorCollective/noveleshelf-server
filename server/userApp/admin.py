from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import User, UserProfile, UserWallet, AdminProfile, AuthorProfile, FreeAuthorProfile, ModeratorProfile, AuthorRequest, EmailVerificationToken, PasswordResetToken, UserFollowAuthor, AuthHandoffToken

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


class UserFollowAuthorInline(admin.TabularInline):
    model = UserFollowAuthor
    extra = 0
    readonly_fields = ['author_profile', 'free_author_profile', 'followed_at']
    can_delete = True
    fk_name = 'user'


class AuthorFollowersInline(admin.TabularInline):
    model = UserFollowAuthor
    extra = 0
    readonly_fields = ['user', 'followed_at']
    can_delete = True
    fk_name = 'author_profile'


class FreeAuthorFollowersInline(admin.TabularInline):
    model = UserFollowAuthor
    extra = 0
    readonly_fields = ['user', 'followed_at']
    can_delete = True
    fk_name = 'free_author_profile'

@admin.register(AuthHandoffToken)
class AuthHandoffTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_used', 'created_at', 'expires_at')
    list_filter = ('is_used',)
    search_fields = ('user__email',)
    readonly_fields = ('user', 'token', 'created_at', 'expires_at', 'is_used')


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'date_of_birth', 'is_staff', 'is_superuser', 'default_login_role']
    inlines = [UserProfileInline, UserWalletInline, AdminProfileInline, AuthorProfileInline, FreeAuthorProfileInline, ModeratorProfileInline, UserFollowAuthorInline]

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


class AuthorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'author_username', 'pen_name', 'tier', 'is_publicly_visible', 'is_active', 'is_featured']
    list_filter = ['tier', 'is_publicly_visible', 'is_active', 'is_featured']
    search_fields = ['user__email', 'author_username', 'pen_name']
    readonly_fields = ['created_at']
    inlines = [AuthorFollowersInline]


class FreeAuthorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'author_username', 'pen_name', 'is_publicly_visible', 'is_active', 'is_featured']
    list_filter = ['is_publicly_visible', 'is_active', 'is_featured']
    search_fields = ['user__email', 'author_username', 'pen_name']
    readonly_fields = ['created_at']
    inlines = [FreeAuthorFollowersInline]


class UserFollowAuthorAdmin(admin.ModelAdmin):
    list_display = ['user', 'author_profile', 'free_author_profile', 'followed_at']
    search_fields = ['user__email']
    readonly_fields = ['followed_at']


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(UserWallet)
admin.site.register(AdminProfile)
admin.site.register(AuthorProfile, AuthorProfileAdmin)
admin.site.register(FreeAuthorProfile, FreeAuthorProfileAdmin)
admin.site.register(ModeratorProfile)
admin.site.register(AuthorRequest, AuthorRequestAdmin)
admin.site.register(EmailVerificationToken)
admin.site.register(PasswordResetToken)
admin.site.register(UserFollowAuthor, UserFollowAuthorAdmin)