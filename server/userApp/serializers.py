from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile, UserWallet, AdminProfile, AuthorProfile, FreeAuthorProfile, ModeratorProfile, AuthorRequest, UserFollowAuthor

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'date_of_birth']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'avatar_url', 'bio', 'created_at']


class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = ['quill_balance', 'gold_ink_balance', 'black_ink_balance', 'updated_at']


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ['admin_username', 'is_super_admin', 'avatar_url', 'created_at']


class AuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorProfile
        fields = ['author_username', 'pen_name', 'first_name', 'last_name', 'show_real_name', 'is_publicly_visible', 'is_active', 'is_featured', 'bio', 'tier', 'contract_link', 'avatar_url', 'created_at']


class FreeAuthorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FreeAuthorProfile
        fields = ['author_username', 'pen_name', 'first_name', 'last_name', 'show_real_name', 'is_publicly_visible', 'is_active', 'is_featured', 'bio', 'avatar_url', 'created_at']


class ModeratorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeratorProfile
        fields = ['mod_username', 'avatar_url', 'assigned_by', 'created_at']


class AuthorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorRequest
        fields = ['id', 'request_type', 'status', 'bio', 'genre_interest', 'writing_sample_link', 'reader_notes', 'created_at', 'updated_at']


class AuthorRequestAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorRequest
        fields = ['id', 'user', 'request_type', 'status', 'bio', 'genre_interest', 'writing_sample_link', 'admin_notes', 'reader_notes', 'contact_attempted', 'created_at', 'updated_at']


class AuthorProfileDashboardSerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField()

    class Meta:
        model = AuthorProfile
        fields = ['author_username', 'pen_name', 'first_name', 'last_name', 'show_real_name', 'is_publicly_visible', 'is_active', 'is_featured', 'bio', 'tier', 'contract_link', 'avatar_url', 'created_at', 'follower_count']

    def get_follower_count(self, obj):
        return obj.followers.count()


class FreeAuthorProfileDashboardSerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField()

    class Meta:
        model = FreeAuthorProfile
        fields = ['author_username', 'pen_name', 'first_name', 'last_name', 'show_real_name', 'is_publicly_visible', 'is_active', 'is_featured', 'bio', 'avatar_url', 'created_at', 'follower_count']

    def get_follower_count(self, obj):
        return obj.followers.count()


class FollowedAuthorProfileSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = AuthorProfile
        fields = ['author_username', 'pen_name', 'display_name', 'avatar_url', 'tier', 'is_publicly_visible']

    def get_display_name(self, obj):
        if obj.show_real_name and obj.first_name:
            return f'{obj.first_name} {obj.last_name}'.strip()
        return obj.pen_name or obj.author_username


class FollowedFreeAuthorProfileSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = FreeAuthorProfile
        fields = ['author_username', 'pen_name', 'display_name', 'avatar_url', 'is_publicly_visible']

    def get_display_name(self, obj):
        if obj.show_real_name and obj.first_name:
            return f'{obj.first_name} {obj.last_name}'.strip()
        return obj.pen_name or obj.author_username


class UserFollowAuthorSerializer(serializers.ModelSerializer):
    author_profile = FollowedAuthorProfileSerializer(read_only=True)
    free_author_profile = FollowedFreeAuthorProfileSerializer(read_only=True)
    author_type = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowAuthor
        fields = ['id', 'author_type', 'author_profile', 'free_author_profile', 'followed_at']

    def get_author_type(self, obj):
        return 'paid' if obj.author_profile else 'free'


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    wallet = UserWalletSerializer(read_only=True)
    admin_profile = AdminProfileSerializer(read_only=True)
    author_profile = AuthorProfileSerializer(read_only=True)
    free_author_profile = FreeAuthorProfileSerializer(read_only=True)
    moderator_profile = ModeratorProfileSerializer(read_only=True)
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'date_of_birth', 'default_login_role', 'is_verified', 'profile', 'wallet', 'admin_profile', 'author_profile', 'free_author_profile', 'moderator_profile', 'following_count']

    def get_following_count(self, obj):
        return obj.following.count()