from rest_framework import serializers
from .models import DailyLoginReward, Transaction


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
        fields = ['last_reward_date', 'total_earned', 'updated_at']