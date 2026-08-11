from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from currencyApp.models import (
    DailyLoginReward, PlatformSettings, Transaction,
    PromoCode, PromoCodeRedemption, QuillBundle, QuillPurchase,
    ReferralCode, ReferralRedemption,
)
from userApp.models import UserWallet


REWARD_CYCLE_LENGTH = 28
SUPER_BONUS_STREAK_DAY = 365
SUPER_BONUS_REWARD = 100
YEARLY_MILESTONE_REWARDS = {
    91: 25,
    182: 50,
    273: 75,
}
BONUS_REWARDS = {
    4: 3,
    7: 4,
    11: 3,
    14: 5,
    18: 3,
    21: 6,
    25: 3,
    28: 7,
}


def _get_next_streak_day(last_reward_date, current_streak_day, today):
    #Return the next day in the true, unbroken login streak (no wrapping —
    #this is the actual streak length, used for display/achievements).
    if last_reward_date == today - timedelta(days=1):
        return current_streak_day + 1

    # A first claim or a missed calendar day starts the streak over.
    return 1

def _get_reward_pattern_day(streak_day):
    #Map an ever-growing streak day onto its position in the repeating
    #365-day reward pattern (day 366 behaves like day 1, day 730 like
    #day 365, etc.) without ever mutating the stored streak itself.
    return ((streak_day - 1) % SUPER_BONUS_STREAK_DAY) + 1


def _get_reward_amount(streak_day, standard_reward):
    #Return the reward for an absolute streak day, based on its position
    #in the repeating 365-day pattern.
    pattern_day = _get_reward_pattern_day(streak_day)

    if pattern_day == SUPER_BONUS_STREAK_DAY:
        return SUPER_BONUS_REWARD

    if pattern_day in YEARLY_MILESTONE_REWARDS:
        return YEARLY_MILESTONE_REWARDS[pattern_day]

    cycle_day = ((pattern_day - 1) % REWARD_CYCLE_LENGTH) + 1
    return BONUS_REWARDS.get(cycle_day, standard_reward)


def process_daily_login_reward(user):
    
    #Award the user's once-per-calendar-day black ink login reward.

    #Consecutive claims advance through a repeating 365-day yearly streak. The
    #normal rewards repeat on a 28-day schedule. Yearly milestones override the
    #normal reward: day 91 awards 25 drops, day 182 awards 50, day 273 awards 75,
    #and day 365 awards 100. The next claim after day 365 begins again at day 1.
    #Missing a calendar day also resets the streak to day 1. Returns True when a
    #reward is granted and False when today's reward was already claimed.
    today = timezone.localdate()

    with transaction.atomic():
        reward, _ = DailyLoginReward.objects.select_for_update().get_or_create(
            user=user
        )

        if reward.last_reward_date == today:
            return False

        streak_day = _get_next_streak_day(
            reward.last_reward_date,
            reward.current_streak_day,
            today,
        )

        settings = PlatformSettings.objects.first()
        standard_reward = settings.daily_black_ink_reward if settings else 2
        reward_amount = _get_reward_amount(streak_day, standard_reward)

        wallet = UserWallet.objects.select_for_update().get(user=user)
        wallet.black_ink_balance += reward_amount
        wallet.save(update_fields=['black_ink_balance', 'updated_at'])

        reward.last_reward_date = today
        reward.current_streak_day = streak_day
        reward.total_earned += reward_amount
        reward.save(update_fields=[
            'last_reward_date',
            'current_streak_day',
            'total_earned',
            'updated_at',
        ])

        # Use the pattern day (not the raw, ever-growing streak_day) so the
        # note correctly says "yearly milestone"/"yearly completion bonus"
        # every time that pattern position recurs (day 91, 456, 821, ...),
        # not just the first time it's ever hit.
        pattern_day = _get_reward_pattern_day(streak_day)
        cycle_day = ((pattern_day - 1) % REWARD_CYCLE_LENGTH) + 1
        notes = f'Daily login reward - streak day {streak_day}'
        if pattern_day == SUPER_BONUS_STREAK_DAY:
            notes += ' (yearly completion bonus)'
        elif pattern_day in YEARLY_MILESTONE_REWARDS:
            notes += ' (yearly milestone bonus)'
        else:
            notes += f' (reward cycle day {cycle_day} of {REWARD_CYCLE_LENGTH})'

        Transaction.objects.create(
            user=user,
            transaction_type='daily_login',
            currency_type='black_ink',
            amount=reward_amount,
            balance_after=wallet.black_ink_balance,
            notes=notes,
        )

    return True


def redeem_promo_code(user, code_input):
    
    #Redeem a promo code for the given user, crediting their wallet.

    #A code can only be redeemed once per user -- enforced by the
    #PromoCodeRedemption (user, promo_code) unique constraint, checked
    #while the PromoCode row itself is locked so two simultaneous
    #redemption attempts for the same code can't both succeed or both
    #push it past its max_redemptions cap.

    #Returns a dict: {'success': bool, 'error': str or None,
    #'amount': int or None, 'currency_type': str or None}.

    #Only black_ink crediting is supported for now.
    code = (code_input or '').strip().upper()
    if not code:
        return {'success': False, 'error_code': 'missing_code', 'error': 'A code is required.', 'amount': None, 'currency_type': None}

    with transaction.atomic():
        try:
            promo_code = PromoCode.objects.select_for_update().get(code=code)
        except PromoCode.DoesNotExist:
            return {'success': False, 'error_code': 'invalid_code', 'error': 'Invalid code.', 'amount': None, 'currency_type': None}

        if not promo_code.is_active:
            return {'success': False, 'error_code': 'inactive', 'error': 'This code is no longer active.', 'amount': None, 'currency_type': None}

        if promo_code.is_expired():
            return {'success': False, 'error_code': 'expired', 'error': 'This code has expired.', 'amount': None, 'currency_type': None}

        if not promo_code.has_redemptions_remaining():
            return {'success': False, 'error_code': 'redemption_limit_reached', 'error': 'This code has reached its redemption limit.', 'amount': None, 'currency_type': None}

        if PromoCodeRedemption.objects.filter(user=user, promo_code=promo_code).exists():
            return {'success': False, 'error_code': 'already_redeemed', 'error': "You've already redeemed this code.", 'amount': None, 'currency_type': None}

        if promo_code.currency_type != 'black_ink':
            # Placeholder guard until Gold Ink / Quills crediting is built out.
            return {'success': False, 'error_code': 'unsupported_currency', 'error': "This code type isn't supported yet.", 'amount': None, 'currency_type': None}

        PromoCodeRedemption.objects.create(user=user, promo_code=promo_code)

        promo_code.times_redeemed += 1
        promo_code.save(update_fields=['times_redeemed', 'updated_at'])

        wallet = UserWallet.objects.select_for_update().get(user=user)
        wallet.black_ink_balance += promo_code.amount
        wallet.save(update_fields=['black_ink_balance', 'updated_at'])

        Transaction.objects.create(
            user=user,
            transaction_type='promo_code',
            currency_type='black_ink',
            amount=promo_code.amount,
            balance_after=wallet.black_ink_balance,
            notes=f'Promo code redemption: {promo_code.code}',
        )

    return {
        'success': True,
        'error_code': None,
        'error': None,
        'amount': promo_code.amount,
        'currency_type': promo_code.currency_type,
    }


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def redeem_promo_code_view(request):
    
    #Endpoint for a user to redeem a promo code (e.g. from a book fair
    #giveaway card). Thin request/response wrapper around the
    #redeem_promo_code() business logic above -- keeps the logic itself
    #testable and reusable without a request object.
    code_input = request.data.get('code')
    result = redeem_promo_code(request.user, code_input)

    if not result['success']:
        error_status = (
            status.HTTP_404_NOT_FOUND
            if result['error_code'] == 'invalid_code'
            else status.HTTP_400_BAD_REQUEST
        )
        return Response({'error': result['error']}, status=error_status)

    return Response({
        'amount': result['amount'],
        'currency_type': result['currency_type'],
    }, status=status.HTTP_200_OK)


def _grant_referral_reward(redemption):

    #Credits both the referrer and referee's black_ink wallets for a
    #ReferralRedemption and stamps rewarded_at. Assumes it's already
    #running inside an outer transaction.atomic() block -- called from
    #both redeem_referral_code() (immediate-reward/backfill case) and
    #apply_pending_referral_reward() (verification-triggered case), so
    #the locking/crediting logic only exists in one place.

    #Locks both wallets in a consistent order (lower user_id first)
    #regardless of which side is the referrer, so two simultaneous
    #referral rewards touching an overlapping pair of users can't
    #deadlock against each other.
    settings = PlatformSettings.objects.first()
    reward_amount = settings.referral_reward_amount if settings else 25

    referrer_id = redemption.referrer_id
    referee_id = redemption.referee_id
    first_id, second_id = sorted([referrer_id, referee_id])

    first_wallet = UserWallet.objects.select_for_update().get(user_id=first_id)
    second_wallet = UserWallet.objects.select_for_update().get(user_id=second_id)

    referrer_wallet = first_wallet if first_id == referrer_id else second_wallet
    referee_wallet = first_wallet if first_id == referee_id else second_wallet

    referrer_wallet.black_ink_balance += reward_amount
    referrer_wallet.save(update_fields=['black_ink_balance', 'updated_at'])

    referee_wallet.black_ink_balance += reward_amount
    referee_wallet.save(update_fields=['black_ink_balance', 'updated_at'])

    Transaction.objects.create(
        user_id=referrer_id,
        transaction_type='referral_reward',
        currency_type='black_ink',
        amount=reward_amount,
        balance_after=referrer_wallet.black_ink_balance,
        notes=f'Referral reward: referred {redemption.referee.email}',
    )

    Transaction.objects.create(
        user_id=referee_id,
        transaction_type='referral_reward',
        currency_type='black_ink',
        amount=reward_amount,
        balance_after=referee_wallet.black_ink_balance,
        notes=f'Referral reward: referred by {redemption.referrer.email}',
    )

    redemption.rewarded_at = timezone.now()
    redemption.save(update_fields=['rewarded_at'])


def redeem_referral_code(referee, code_input):

    #Redeem a friend's referral code for the given referee. Covers both
    #entry points -- signup time and backfill (a reader entering a
    #friend's code later from Settings) -- since the only real
    #difference between them is whether referee.is_verified is already
    #True. If it is, the reward pays out immediately (the backfill
    #case). If not, redemption is recorded and the reward waits for
    #apply_pending_referral_reward() to be called once verification
    #completes.

    #A referee can only ever redeem one referral code, ever -- enforced
    #by the ReferralRedemption.referee OneToOneField, checked explicitly
    #here first for a clean error message rather than relying on the
    #IntegrityError. Self-referral is blocked the same way.

    #Returns a dict: {'success': bool, 'error_code': str or None,
    #'error': str or None, 'rewarded_immediately': bool}.
    code = (code_input or '').strip().upper()
    if not code:
        return {'success': False, 'error_code': 'missing_code', 'error': 'A code is required.', 'rewarded_immediately': False}

    with transaction.atomic():
        try:
            referral_code = ReferralCode.objects.select_for_update().get(code=code)
        except ReferralCode.DoesNotExist:
            return {'success': False, 'error_code': 'invalid_code', 'error': 'Invalid referral code.', 'rewarded_immediately': False}

        referrer = referral_code.user

        if referrer.id == referee.id:
            return {'success': False, 'error_code': 'self_referral', 'error': "You can't redeem your own referral code.", 'rewarded_immediately': False}

        if ReferralRedemption.objects.filter(referee=referee).exists():
            return {'success': False, 'error_code': 'already_redeemed', 'error': "You've already redeemed a referral code.", 'rewarded_immediately': False}

        redemption = ReferralRedemption.objects.create(
            referrer=referrer,
            referee=referee,
        )

        if referee.is_verified:
            _grant_referral_reward(redemption)
            return {'success': True, 'error_code': None, 'error': None, 'rewarded_immediately': True}

    return {'success': True, 'error_code': None, 'error': None, 'rewarded_immediately': False}


def apply_pending_referral_reward(user):

    #Call this once a user's email verification completes (i.e.
    #wherever User.is_verified gets set to True). Checks whether this
    #user redeemed a referral code as a referee before they were
    #verified, and if so, pays out the reward now. No-op if there's no
    #pending redemption, or if it's already been rewarded -- safe to
    #call unconditionally from the verification flow rather than
    #needing to check first.

    #Returns True if a reward was granted, False otherwise.
    with transaction.atomic():
        redemption = (
            ReferralRedemption.objects
            .select_for_update()
            .filter(referee=user, rewarded_at__isnull=True)
            .first()
        )

        if not redemption:
            return False

        _grant_referral_reward(redemption)

    return True


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def redeem_referral_code_view(request):

    #Endpoint for a reader to redeem a friend's referral code -- either
    #during registration (called directly, not through this view, since
    #there's no JWT yet at that point) or via backfill from Settings
    #after the fact (this view, for an already-authenticated user).
    code_input = request.data.get('code')
    result = redeem_referral_code(request.user, code_input)

    if not result['success']:
        error_status = (
            status.HTTP_404_NOT_FOUND
            if result['error_code'] == 'invalid_code'
            else status.HTTP_400_BAD_REQUEST
        )
        return Response({'error': result['error']}, status=error_status)

    return Response({
        'rewarded_immediately': result['rewarded_immediately'],
    }, status=status.HTTP_200_OK)


def credit_quill_purchase(user, quill_bundle_id, stripe_session_id, stripe_event_id, stripe_payment_intent_id, amount_paid_cents, currency='usd'):
    
    #Credits a user's Quills wallet after a Stripe checkout.session.completed
    #webhook confirms payment. Idempotent -- safe to call more than once with
    #the same stripe_event_id, since Stripe can and will redeliver webhooks.

    #Returns a dict: {'success': bool, 'error_code': str or None,
    #'error': str or None, 'quill_purchase': QuillPurchase or None}.
    
    existing = QuillPurchase.objects.filter(stripe_event_id=stripe_event_id).first()
    if existing:
        return {'success': True, 'error_code': None, 'error': None, 'quill_purchase': existing}

    with transaction.atomic():
        try:
            bundle = QuillBundle.objects.get(id=quill_bundle_id, is_active=True)
        except QuillBundle.DoesNotExist:
            return {'success': False, 'error_code': 'invalid_bundle', 'error': 'Quill bundle not found or inactive.', 'quill_purchase': None}

        wallet = UserWallet.objects.select_for_update().get(user=user)
        wallet.quill_balance += bundle.quills
        wallet.save(update_fields=['quill_balance', 'updated_at'])

        txn = Transaction.objects.create(
            user=user,
            transaction_type='quill_purchase',
            currency_type='quills',
            amount=bundle.quills,
            balance_after=wallet.quill_balance,
            notes=f'Stripe purchase: {bundle.name}',
        )

        purchase = QuillPurchase.objects.create(
            user=user,
            quill_bundle=bundle,
            transaction=txn,
            stripe_checkout_session_id=stripe_session_id,
            stripe_payment_intent_id=stripe_payment_intent_id,
            stripe_event_id=stripe_event_id,
            amount_paid_cents=amount_paid_cents,
            currency=currency,
            status='completed',
        )

    return {'success': True, 'error_code': None, 'error': None, 'quill_purchase': purchase}