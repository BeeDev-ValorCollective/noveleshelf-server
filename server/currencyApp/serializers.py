from rest_framework import serializers
from .models import DailyLoginReward, Transaction, FoundingAuthorSlot


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'id', 'transaction_type', 'currency_type',
            'amount', 'balance_after', 'notes', 'created_at'
        ]


class DailyLoginRewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLoginReward
        fields = [
            'last_reward_date', 'current_streak_day', 'total_earned', 'updated_at',
        ]
        read_only_fields = [
            'last_reward_date', 'current_streak_day', 'total_earned', 'updated_at',
        ]


class FoundingAuthorBadgeSerializer(serializers.ModelSerializer):
    """
    Public-safe founding-author shape — no slot_number, no assigned_at,
    no eligible_books. Just enough for an author (or eventually a reader)
    to see "this author is a founding author" plus what the bonus covers.

    Nest this with source='founding_author_slot' wherever AuthorProfile
    is serialized. If the author has no slot, the reverse relation
    resolves to None — the calling serializer is responsible for
    omitting the field entirely in that case (see
    AuthorProfileSerializer.to_representation for the pattern).
    """
    bonus_percent = serializers.DecimalField(source='bonus_tier.percent', max_digits=4, decimal_places=2)
    duration_label = serializers.CharField(source='duration.label')

    class Meta:
        model = FoundingAuthorSlot
        fields = ['bonus_percent', 'duration_label']