# statsApp/utils.py
from django.db import models as db_models
from django.utils import timezone
from .models import DailyActivity, Event


def record_daily_activity(user, activity_type, platform='unknown'):
    """
    Safe to call multiple times a day — creates one row per
    (user, activity_type, platform, date) and bumps occurrence_count on
    repeat calls for that same combination.
    """
    today = timezone.localdate()
    activity, created = DailyActivity.objects.get_or_create(
        user=user,
        activity_type=activity_type,
        platform=platform,
        date=today,
        defaults={'occurrence_count': 1},
    )
    if not created:
        DailyActivity.objects.filter(pk=activity.pk).update(
            occurrence_count=db_models.F('occurrence_count') + 1
        )
    return activity


def log_event(user, event_type, platform='unknown', **metadata):
    """
    Fire-and-forget event log. user can be None for anonymous/public actions
    (e.g. an unauthenticated visitor browsing the public library).
    """
    Event.objects.create(
        user=user if user and user.is_authenticated else None,
        event_type=event_type,
        platform=platform,
        metadata=metadata or None,
    )