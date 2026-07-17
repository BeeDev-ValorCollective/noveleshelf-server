# currencyApp/urls.py
from django.urls import path
from currencyApp.views.admin_views import (
    admin_add_currency, admin_gift_currency,
    admin_create_promo_code, admin_update_promo_code, admin_list_promo_codes,
)
from currencyApp.views.reward_views import redeem_promo_code_view

# api/currency/

urlpatterns = [
    path('admin/add/', admin_add_currency, name='admin-add-currency'),
    path('admin/gift/', admin_gift_currency, name='admin-gift-currency'),
    path('promo/redeem/', redeem_promo_code_view, name='redeem-promo-code'),
    path('promo/admin/create/', admin_create_promo_code, name='admin-create-promo-code'),
    path('promo/admin/<str:code>/update/', admin_update_promo_code, name='admin-update-promo-code'),
    path('promo/admin/list/', admin_list_promo_codes, name='admin-list-promo-codes'),
]