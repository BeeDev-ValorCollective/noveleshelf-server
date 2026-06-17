from django.db import models


class DailyLoginReward(models.Model):
    user = models.OneToOneField(
        'userApp.User',
        on_delete=models.CASCADE,
        related_name='daily_login_reward'
    )
    last_reward_date = models.DateField(null=True, blank=True)
    total_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} daily reward'


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('daily_login', 'Daily Login Reward'),
        ('ad_reward', 'Ad Reward'),
        ('quill_purchase', 'Quill Purchase'),
        ('chapter_unlock', 'Chapter Unlock'),
        ('author_payout', 'Author Payout'),
        ('admin_adjustment', 'Admin Adjustment'),
        ('admin_gift', 'Admin Gift'),
    ]

    CURRENCY_TYPES = [
        ('black_ink', 'Black Ink Drop'),
        ('gold_ink', 'Gold Ink Drop'),
        ('quills', 'Quills'),
    ]

    user = models.ForeignKey(
        'userApp.User',
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    currency_type = models.CharField(max_length=10, choices=CURRENCY_TYPES)
    amount = models.IntegerField()
    balance_after = models.IntegerField()
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.email} — {self.transaction_type} — {self.amount} {self.currency_type}'
    
class PlatformSettings(models.Model):
    daily_black_ink_reward = models.IntegerField(default=2)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Platform Settings'
        verbose_name_plural = 'Platform Settings'

    def __str__(self):
        return 'Platform Settings'