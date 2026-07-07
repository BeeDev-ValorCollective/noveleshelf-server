from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from userApp.models import User, UserWallet
from currencyApp.models import Transaction


class AdminAddCurrencyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not hasattr(request.user, 'admin_profile') or not request.user.admin_profile.is_super_admin:
            return Response({'detail': 'Super admin access required.'}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        currency_type = request.data.get('currency_type')
        amount = request.data.get('amount')
        notes = request.data.get('notes', 'Manual admin credit')

        if not all([user_id, currency_type, amount]):
            return Response({'detail': 'user_id, currency_type, and amount are required.'}, status=status.HTTP_400_BAD_REQUEST)

        VALID_TYPES = ['black_ink', 'gold_ink', 'quills']
        if currency_type not in VALID_TYPES:
            return Response({'detail': f'currency_type must be one of: {", ".join(VALID_TYPES)}'}, status=status.HTTP_400_BAD_REQUEST)

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

class AdminGiftCurrencyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
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