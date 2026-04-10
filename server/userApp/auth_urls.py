from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import auth_views

urlpatterns = [
    path('register/', auth_views.register),
    path('login/', auth_views.login),
    path('logout/', auth_views.logout),
    path('me/', auth_views.me),
    path('refresh/', TokenRefreshView.as_view()),
]