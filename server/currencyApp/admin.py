from django.contrib import admin
from .models import DailyLoginReward, Transaction, PlatformSettings


@admin.register(DailyLoginReward)
class DailyLoginRewardAdmin(admin.ModelAdmin):
    list_display = ['user', 'last_reward_date', 'total_earned', 'updated_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'currency_type', 'amount', 'balance_after', 'created_at']
    search_fields = ['user__email']
    list_filter = ['transaction_type', 'currency_type']
    readonly_fields = ['created_at']

@admin.register(PlatformSettings)
class PlatformSettingsAdmin(admin.ModelAdmin):
    list_display = ['daily_black_ink_reward', 'updated_at']