from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    default_login_role = models.CharField(
        max_length=20,
        choices=[
            ('reader', 'Reader'),
            ('free_author', 'Free Author'),
            ('author', 'Author'),
            ('moderator', 'Moderator'),
            ('admin', 'Admin'),
        ],
        default='reader',
        null=True,
        blank=True
    )
    is_verified = models.BooleanField(default=False)
    verification_grace_ends = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    avatar_url = models.ImageField(
        upload_to='avatars/reader/', 
        null=True, 
        blank=True,
        default='avatars/reader/default.png'
    )
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} profile'

class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    quill_balance = models.IntegerField(default=0)
    gold_ink_balance = models.IntegerField(default=0)
    black_ink_balance = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} wallet'

class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    admin_username = models.CharField(max_length=50, unique=True)
    is_super_admin = models.BooleanField(default=False)
    avatar_url = models.ImageField(
        upload_to='avatars/admin/',
        null=True,
        blank=True,
        default='avatars/admin/default.png'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.admin_username} ({"super " if self.is_super_admin else ""}admin)'
    
class AuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='author_profile')
    author_username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    pen_name = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    show_real_name = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    bio = models.TextField(null=True, blank=True)
    tier = models.IntegerField(default=1)
    contract_link = models.URLField(null=True, blank=True)
    is_publicly_visible = models.BooleanField(default=False)
    avatar_url = models.ImageField(
        upload_to='avatars/author/',
        null=True,
        blank=True,
        default='avatars/author/default.png'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pen_name or self.author_username or self.user.email} (author)'
    
class FreeAuthorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='free_author_profile')
    author_username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    pen_name = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    show_real_name = models.BooleanField(default=False)
    is_publicly_visible = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    bio = models.TextField(null=True, blank=True)
    avatar_url = models.ImageField(
        upload_to='avatars/free_author/',
        null=True,
        blank=True,
        default='avatars/free_author/default.png'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pen_name or self.author_username or self.user.email} (free author)'

class ModeratorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='moderator_profile')
    mod_username = models.CharField(max_length=50, unique=True, null=True, blank=True)
    avatar_url = models.ImageField(
        upload_to='avatars/moderator/',
        null=True,
        blank=True,
        default='avatars/moderator/default.png'
    )
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_moderators'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.mod_username or self.user.email} (moderator)'
    
class AuthorRequest(models.Model):
    REQUEST_TYPES = [
        ('new_author', 'New Author'),
        ('new_genre', 'New Genre'),
        ('tier_review', 'Tier Review'),
        ('contract_addendum', 'Contract Addendum'),
        ('leave_platform', 'Leave Platform'),
        ('rejoin_platform', 'Rejoin Platform'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('approved', 'Approved'),
        ('not_at_this_time', 'Not At This Time'),
        ('cleared', 'Cleared'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_requests')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    bio = models.TextField(null=True, blank=True)
    genre_interest = models.CharField(max_length=100, null=True, blank=True)
    writing_sample_link = models.URLField(null=True, blank=True)
    admin_notes = models.TextField(null=True, blank=True)
    reader_notes = models.TextField(null=True, blank=True)
    contact_attempted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} - {self.request_type} ({self.status})'
    
class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verification_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.email} verification token'