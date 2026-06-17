from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Sum, Count
from currencyApp.models import Transaction


def _require_admin(request):
    """Returns an error Response if the user isn't an admin, otherwise None."""
    if not hasattr(request.user, 'admin_profile'):
        return Response({'detail': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)
    return None


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_log(request):
    admin_error = _require_admin(request)
    if admin_error:
        return admin_error

    queryset = Transaction.objects.all()

    user_id = request.query_params.get('user_id')
    if user_id:
        queryset = queryset.filter(user_id=user_id)

    transaction_type = request.query_params.get('transaction_type')
    if transaction_type:
        queryset = queryset.filter(transaction_type=transaction_type)

    currency_type = request.query_params.get('currency_type')
    if currency_type:
        queryset = queryset.filter(currency_type=currency_type)

    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to')
    if date_from:
        queryset = queryset.filter(created_at__date__gte=date_from)
    if date_to:
        queryset = queryset.filter(created_at__date__lte=date_to)
    elif date_from:
        # date_from with no date_to means "just that single day"
        queryset = queryset.filter(created_at__date=date_from)

    paginator = PageNumberPagination()
    paginator.page_size = 25
    page = paginator.paginate_queryset(queryset, request)

    results = [
        {
            'id': txn.id,
            'user_id': txn.user_id,
            'user_email': txn.user.email,
            'transaction_type': txn.transaction_type,
            'currency_type': txn.currency_type,
            'amount': txn.amount,
            'balance_after': txn.balance_after,
            'notes': txn.notes,
            'created_at': txn.created_at,
        }
        for txn in page
    ]

    return paginator.get_paginated_response(results)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_totals(request):
    admin_error = _require_admin(request)
    if admin_error:
        return admin_error

    queryset = Transaction.objects.all()

    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to')
    if date_from:
        queryset = queryset.filter(created_at__date__gte=date_from)
    if date_to:
        queryset = queryset.filter(created_at__date__lte=date_to)
    elif date_from:
        queryset = queryset.filter(created_at__date=date_from)

    totals = {
        choice_value: {'count': 0, 'total_amount': 0}
        for choice_value, _label in Transaction.TRANSACTION_TYPES
    }

    aggregated = (
        queryset
        .values('transaction_type')
        .annotate(count=Count('id'), total_amount=Sum('amount'))
    )

    for row in aggregated:
        totals[row['transaction_type']] = {
            'count': row['count'],
            'total_amount': row['total_amount'] or 0,
        }

    return Response(totals, status=status.HTTP_200_OK)