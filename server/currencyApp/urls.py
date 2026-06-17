# currencyApp/urls.py
from django.urls import path
from currencyApp.views.admin_views import AdminAddCurrencyView, AdminGiftCurrencyView

urlpatterns = [
    path('admin/add/', AdminAddCurrencyView.as_view(), name='admin-add-currency'),
    path('admin/gift/', AdminGiftCurrencyView.as_view(), name='admin-gift-currency'),
]