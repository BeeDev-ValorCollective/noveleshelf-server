# statsApp/urls/admin_urls.py
from django.urls import path
from statsApp.views import admin_views

# api/stats/admin/

urlpatterns = [
    path('transactions/', admin_views.transaction_log),
    path('transactions/totals/', admin_views.transaction_totals),
]