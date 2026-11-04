from django.db import models


class NotificationType(models.Model):
    RECIPIENT_CHOICES = [
        ('user', 'User Only'),
        ('admin', 'Admin Only'),
        ('both', 'Both User and Admin'),
    ]

    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    description = models.TextField()
    recipient_type = models.CharField(max_length=10, choices=RECIPIENT_CHOICES, default='admin')
    sends_to_user = models.BooleanField(default=False)
    sends_to_admins = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.label} ({self.code})'

    class Meta:
        ordering = ['label']


class NotificationPreference(models.Model):
    user = models.ForeignKey(
        'userApp.User',
        on_delete=models.CASCADE,
        related_name='notification_preferences'
    )
    notification_type = models.ForeignKey(
        NotificationType,
        on_delete=models.CASCADE,
        related_name='preferences'
    )
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'notification_type')

    def __str__(self):
        return f'{self.user.email} - {self.notification_type.label} - {"On" if self.is_enabled else "Off"}'


class NotificationPermission(models.Model):
    user = models.ForeignKey(
        'userApp.User',
        on_delete=models.CASCADE,
        related_name='notification_permissions'
    )
    notification_type = models.ForeignKey(
        NotificationType,
        on_delete=models.CASCADE,
        related_name='permissions'
    )
    granted_by = models.ForeignKey(
        'userApp.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='granted_permissions'
    )
    is_allowed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'notification_type')

    def __str__(self):
        return f'{self.user.email} - {self.notification_type.label} - {"Allowed" if self.is_allowed else "Not Allowed"}'


class SystemNotificationEmail(models.Model):
    email = models.EmailField(unique=True)
    label = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    notification_types = models.ManyToManyField(
        NotificationType,
        related_name='system_emails',
        blank=True
    )
    created_by = models.ForeignKey(
        'userApp.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_system_emails'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.label} ({self.email})'



class Notification(models.Model):
    user = models.ForeignKey(
        'userApp.User',
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    notification_type = models.ForeignKey(
        NotificationType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='notifications'
    )

    title = models.CharField(
        max_length=200,
        blank=True,
        default=''
    )

    message = models.TextField()

    book = models.ForeignKey(
        'booksApp.Book',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_notifications'
    )

    chapter = models.ForeignKey(
        'booksApp.Chapter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_notifications'
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        notification_name = (
            self.notification_type.label
            if self.notification_type
            else self.title or 'Notification'
        )

        read_status = (
            'Read' if self.is_read else 'Unread'
        )

        return (
            f'{self.user.email} - '
            f'{notification_name} - '
            f'{read_status}'
        )
