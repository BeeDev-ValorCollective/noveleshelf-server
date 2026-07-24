# currencyApp/urls.py
from django.urls import path
from currencyApp.views.admin_views import (
    admin_add_currency, admin_gift_currency,
    admin_create_promo_code, admin_update_promo_code, admin_list_promo_codes,
)
from currencyApp.views.reward_views import redeem_promo_code_view
from currencyApp.views.stripe_views import (
    list_quill_bundles, create_quill_checkout, stripe_webhook,
)

# api/currency/

urlpatterns = [
    path('admin/add/', admin_add_currency, name='admin-add-currency'),
    path('admin/gift/', admin_gift_currency, name='admin-gift-currency'),
    path('promo/redeem/', redeem_promo_code_view, name='redeem-promo-code'),
    path('promo/admin/create/', admin_create_promo_code, name='admin-create-promo-code'),
    path('promo/admin/<str:code>/update/', admin_update_promo_code, name='admin-update-promo-code'),
    path('promo/admin/list/', admin_list_promo_codes, name='admin-list-promo-codes'),
    path('quills/bundles/', list_quill_bundles, name='list-quill-bundles'),
    path('quills/checkout/create/', create_quill_checkout, name='create-quill-checkout'),
    path('quills/webhook/', stripe_webhook, name='stripe-webhook'),
]