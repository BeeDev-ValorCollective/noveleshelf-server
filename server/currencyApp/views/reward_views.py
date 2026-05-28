from django.utils import timezone
from currencyApp.models import DailyLoginReward, Transaction, PlatformSettings

def process_daily_login_reward(user):
    """
    Call this on every /me/ request.
    Awards black ink drops if user hasn't earned today.
    Amount is set in PlatformSettings via Django admin.
    Returns True if reward was given, False if already earned today.
    """
    today = timezone.now().date()

    try:
        reward = user.daily_login_reward
    except DailyLoginReward.DoesNotExist:
        reward = DailyLoginReward.objects.create(user=user)

    if reward.last_reward_date == today:
        return False

    settings = PlatformSettings.objects.first()
    reward_amount = settings.daily_black_ink_reward if settings else 2

    wallet = user.wallet
    wallet.black_ink_balance += reward_amount
    wallet.save()

    reward.last_reward_date = today
    reward.total_earned += reward_amount
    reward.save()

    Transaction.objects.create(
        user=user,
        transaction_type='daily_login',
        currency_type='black_ink',
        amount=reward_amount,
        balance_after=wallet.black_ink_balance,
        notes='Daily login reward'
    )

    return True