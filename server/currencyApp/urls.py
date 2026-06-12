from django.urls import path
from currencyApp.views.admin_views import AdminAddCurrencyView

urlpatterns = [
    path('admin/add/', AdminAddCurrencyView.as_view(), name='admin-add-currency'),
]