"""
Shared sorting + pagination for admin list endpoints
(user management, author requests, book approvals).

Query params:
    page       1-based page number (default 1)
    page_size  one of ADMIN_PAGE_SIZES (anything else falls back to default_size)
    order      key into the view's `fields` map, e.g. 'newest', 'oldest', 'az', 'za'
"""

ADMIN_PAGE_SIZES = {10, 25, 50, 100}


def admin_order(request, queryset, fields):
    """
    fields maps an `order` value to a model field, e.g.
    {'newest': '-date_joined', 'oldest': 'date_joined', 'az': 'email', 'za': '-email'}.
    Unknown values fall back to 'newest'. 'id' is a tie-breaker so rows with the
    same sort value can't shift between pages.
    """
    order = request.query_params.get('order', 'newest')
    field = fields.get(order, fields['newest'])
    tie_breaker = '-id' if field.startswith('-') else 'id'
    return queryset.order_by(field, tie_breaker)


def admin_paginate(request, queryset, serializer_class, default_size=20):
    try:
        page = max(int(request.query_params.get('page', 1)), 1)
    except ValueError:
        page = 1

    try:
        page_size = int(request.query_params.get('page_size', default_size))
    except ValueError:
        page_size = default_size
    if page_size not in ADMIN_PAGE_SIZES:
        page_size = default_size

    total = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size

    return {
        'count': total,
        'page': page,
        'page_size': page_size,
        'total_pages': (total + page_size - 1) // page_size,
        'next': f'?page={page + 1}' if end < total else None,
        'previous': f'?page={page - 1}' if page > 1 else None,
        'results': serializer_class(queryset[start:end], many=True).data,
    }
