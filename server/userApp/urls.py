from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('refresh/', TokenRefreshView.as_view()),
    path('me/', views.me),
    path('profile/update/', views.update_profile),
    path('admin-profile/update/', views.update_admin_profile),
    path('admin/author-upgrade/', views.upgrade_to_author),
]