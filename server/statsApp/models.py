# statsApp/models.py
from django.db import models


class DailyActivity(models.Model):
    """
    One row per (user, activity_type, platform, date). The row's mere
    existence means the user did that activity at least once that day, on
    that platform — so "days logged in" is
    DailyActivity.objects.filter(user=u, activity_type='login').count()
    across all platforms, or add platform=... to scope to one client.

    occurrence_count is a same-day tally (e.g. chapters read that day) for
    future metrics that need volume, not just presence — bump it instead of
    creating duplicate rows for the same day/platform.
    """
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('read', 'Read'),
    ]

    user = models.ForeignKey('userApp.User', on_delete=models.CASCADE, related_name='daily_activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    platform = models.CharField(max_length=20, default='unknown')
    date = models.DateField()
    occurrence_count = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'activity_type', 'platform', 'date')
        ordering = ['-date']
        verbose_name = 'Daily Activity'
        verbose_name_plural = 'Daily Activities'
        indexes = [
            models.Index(fields=['user', 'activity_type']),
        ]

    def __str__(self):
        return f'{self.user.email} — {self.activity_type} — {self.platform} — {self.date}'


class Event(models.Model):
    """
    Generic raw event log — one row per user action. Deliberately unopinionated
    about what "matters" yet: log liberally now, decide what's useful once
    there's actual usage data to look at.

    event_type is a free-standing string, not a choices field — new event
    types should be addable from any app without a migration here. Document
    the vocabulary in code comments near each log_event() call site instead.

    platform is likewise a free string ('vite', 'expo_web', 'expo_native',
    etc.) rather than choices, so a new client type never needs a migration.

    metadata holds whatever context is relevant to that event type (book_id,
    search query, filter params, etc.) — keep it small and JSON-serializable.

    user is nullable so anonymous/public actions (e.g. an unauthenticated
    visitor browsing the public library) can still be logged, not skipped.
    """
    user = models.ForeignKey(
        'userApp.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
    )
    event_type = models.CharField(max_length=50)
    platform = models.CharField(max_length=20, default='unknown')
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['user', 'event_type']),
            models.Index(fields=['platform']),
        ]

    def __str__(self):
        return f'{self.user.email if self.user else "anon"} — {self.event_type} — {self.platform} — {self.created_at}'