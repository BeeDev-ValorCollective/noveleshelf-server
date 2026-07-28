from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from userApp.views import auth_views

# api/auth/

urlpatterns = [
    path('register/', auth_views.register),
    path('login/', auth_views.login),
    path('logout/', auth_views.logout),
    path('me/', auth_views.me),
    path('refresh/', TokenRefreshView.as_view()),
    path('verify-email/', auth_views.verify_email),
    path('resend-verification/', auth_views.resend_verification),
    path('forgot-password/', auth_views.forgot_password),
    path('reset-password/', auth_views.reset_password),
    path('create-handoff-token/', auth_views.create_handoff_token),
    path('exchange-handoff-token/', auth_views.exchange_handoff_token),
]