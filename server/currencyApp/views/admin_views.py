from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.dateparse import parse_datetime
from userApp.models import User, UserWallet
from currencyApp.models import Transaction, PromoCode


VALID_CURRENCY_TYPES = ['black_ink', 'gold_ink', 'quills']


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_add_currency(request):
    if not hasattr(request.user, 'admin_profile') or not request.user.admin_profile.is_super_admin:
        return Response({'detail': 'Super admin access required.'}, status=status.HTTP_403_FORBIDDEN)

    user_id = request.data.get('user_id')
    currency_type = request.data.get('currency_type')
    amount = request.data.get('amount')
    notes = request.data.get('notes', 'Manual admin credit')

    if not all([user_id, currency_type, amount]):
        return Response({'detail': 'user_id, currency_type, and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if currency_type not in VALID_CURRENCY_TYPES:
        return Response({'detail': f'currency_type must be one of: {", ".join(VALID_CURRENCY_TYPES)}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        amount = int(amount)
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return Response({'detail': 'amount must be a positive integer.'}, status=status.HTTP_400_BAD_REQUEST)

    target_user = get_object_or_404(User, id=user_id)
    wallet, _ = UserWallet.objects.get_or_create(user=target_user)

    if currency_type == 'black_ink':
        wallet.black_ink_balance += amount
        balance_after = wallet.black_ink_balance
    elif currency_type == 'gold_ink':
        wallet.gold_ink_balance += amount
        balance_after = wallet.gold_ink_balance
    else:
        wallet.quill_balance += amount
        balance_after = wallet.quill_balance

    wallet.save()

    Transaction.objects.create(
        user=target_user,
        transaction_type='admin_adjustment',
        currency_type=currency_type,
        amount=amount,
        balance_after=balance_after,
        notes=f'{notes} (added by {request.user.email})'
    )

    return Response({
        'detail': f'Added {amount} {currency_type} to {target_user.email}.',
        'wallet': {
            'quill_balance': wallet.quill_balance,
            'gold_ink_balance': wallet.gold_ink_balance,
            'black_ink_balance': wallet.black_ink_balance,
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_gift_currency(request):
    if not hasattr(request.user, 'admin_profile'):
        return Response({'detail': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)

    user_id = request.data.get('user_id')
    amount = request.data.get('amount')
    notes = request.data.get('notes', 'Admin gift')

    if not all([user_id, amount]):
        return Response({'detail': 'user_id and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        amount = int(amount)
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return Response({'detail': 'amount must be a positive integer.'}, status=status.HTTP_400_BAD_REQUEST)

    target_user = get_object_or_404(User, id=user_id)
    wallet, _ = UserWallet.objects.get_or_create(user=target_user)

    wallet.black_ink_balance += amount
    wallet.save()

    Transaction.objects.create(
        user=target_user,
        transaction_type='admin_gift',
        currency_type='black_ink',
        amount=amount,
        balance_after=wallet.black_ink_balance,
        notes=f'{notes} (gifted by {request.user.email})'
    )

    return Response({
        'detail': f'Gifted {amount} black ink drops to {target_user.email}.',
        'wallet': {
            'quill_balance': wallet.quill_balance,
            'gold_ink_balance': wallet.gold_ink_balance,
            'black_ink_balance': wallet.black_ink_balance,
        }
    }, status=status.HTTP_200_OK)


def _serialize_promo_code(promo_code):
    return {
        'code': promo_code.code,
        'currency_type': promo_code.currency_type,
        'amount': promo_code.amount,
        'is_active': promo_code.is_active,
        'expires_at': promo_code.expires_at,
        'max_redemptions': promo_code.max_redemptions,
        'times_redeemed': promo_code.times_redeemed,
        'created_at': promo_code.created_at,
        'updated_at': promo_code.updated_at,
    }


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_create_promo_code(request):
    if not hasattr(request.user, 'admin_profile'):
        return Response({'detail': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)

    code = request.data.get('code')
    currency_type = request.data.get('currency_type', 'black_ink')
    amount = request.data.get('amount')
    expires_at = request.data.get('expires_at')  # optional ISO 8601 string
    max_redemptions = request.data.get('max_redemptions')  # optional, null/omitted = unlimited

    if not all([code, amount]):
        return Response({'detail': 'code and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if currency_type not in VALID_CURRENCY_TYPES:
        return Response({'detail': f'currency_type must be one of: {", ".join(VALID_CURRENCY_TYPES)}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        amount = int(amount)
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return Response({'detail': 'amount must be a positive integer.'}, status=status.HTTP_400_BAD_REQUEST)

    if max_redemptions in (None, ''):
        max_redemptions = None
    else:
        try:
            max_redemptions = int(max_redemptions)
            if max_redemptions <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return Response({'detail': 'max_redemptions must be a positive integer, or omitted for unlimited.'}, status=status.HTTP_400_BAD_REQUEST)

    parsed_expires_at = None
    if expires_at:
        parsed_expires_at = parse_datetime(expires_at)
        if parsed_expires_at is None:
            return Response({'detail': 'expires_at must be a valid ISO 8601 datetime.'}, status=status.HTTP_400_BAD_REQUEST)

    # Normalize casing before validation (not just relying on the model's
    # save() override) so validate_unique() below actually checks against
    # the same casing that will be stored, instead of missing a collision
    # like "bookfair26" vs an existing "BOOKFAIR26".
    normalized_code = code.strip().upper()

    promo_code = PromoCode(
        code=normalized_code,
        currency_type=currency_type,
        amount=amount,
        expires_at=parsed_expires_at,
        max_redemptions=max_redemptions,
    )

    try:
        promo_code.full_clean()
    except ValidationError as e:
        return Response({'detail': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    try:
        promo_code.save()
    except IntegrityError:
        # Safety net for a rare race between the check above and the
        # actual insert -- not expected in normal use.
        return Response({'detail': 'A code with this value already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(_serialize_promo_code(promo_code), status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def admin_update_promo_code(request, code):
    if not hasattr(request.user, 'admin_profile'):
        return Response({'detail': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)

    normalized_code = (code or '').strip().upper()
    promo_code = get_object_or_404(PromoCode, code=normalized_code)

    # times_redeemed is a system-maintained counter, not admin-editable.
    # code itself is immutable once created -- make a new code instead of
    # renaming one that may already have redemptions tied to it. Renaming
    # is disallowed on purpose to keep PromoCodeRedemption's audit trail
    # trustworthy.
    EDITABLE_FIELDS = ['currency_type', 'amount', 'is_active', 'expires_at', 'max_redemptions']

    for field in EDITABLE_FIELDS:
        if field not in request.data:
            continue

        value = request.data[field]

        if field == 'currency_type':
            if value not in VALID_CURRENCY_TYPES:
                return Response({'detail': f'currency_type must be one of: {", ".join(VALID_CURRENCY_TYPES)}'}, status=status.HTTP_400_BAD_REQUEST)

        elif field == 'amount':
            try:
                value = int(value)
                if value <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                return Response({'detail': 'amount must be a positive integer.'}, status=status.HTTP_400_BAD_REQUEST)

        elif field == 'max_redemptions':
            if value in (None, ''):
                value = None
            else:
                try:
                    value = int(value)
                    if value <= 0:
                        raise ValueError
                except (ValueError, TypeError):
                    return Response({'detail': 'max_redemptions must be a positive integer, or null for unlimited.'}, status=status.HTTP_400_BAD_REQUEST)

        elif field == 'expires_at':
            if value in (None, ''):
                value = None
            else:
                parsed = parse_datetime(value)
                if parsed is None:
                    return Response({'detail': 'expires_at must be a valid ISO 8601 datetime.'}, status=status.HTTP_400_BAD_REQUEST)
                value = parsed

        setattr(promo_code, field, value)

    try:
        promo_code.full_clean(exclude=['code'])
    except ValidationError as e:
        return Response({'detail': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)

    promo_code.save()

    return Response(_serialize_promo_code(promo_code), status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_list_promo_codes(request):
    if not hasattr(request.user, 'admin_profile'):
        return Response({'detail': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)

    codes = PromoCode.objects.all().order_by('-created_at')

    is_active_param = request.query_params.get('is_active')
    if is_active_param is not None:
        if is_active_param.lower() == 'true':
            codes = codes.filter(is_active=True)
        elif is_active_param.lower() == 'false':
            codes = codes.filter(is_active=False)

    return Response([_serialize_promo_code(c) for c in codes], status=status.HTTP_200_OK)