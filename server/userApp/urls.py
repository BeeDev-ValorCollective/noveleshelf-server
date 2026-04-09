from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('refresh/', TokenRefreshView.as_view()),
    path('me/', views.me),
    # Update Profile Routes
    path('profile/update/', views.update_profile),
    path('author-profile/update/', views.update_author_profile),
    path('admin-profile/update/', views.update_admin_profile),
    path('moderator-profile/update/', views.update_moderator_profile),
    # Admin Routes
    path('admin/author-upgrade/', views.upgrade_to_author),
    path('admin/author-profile/update/', views.admin_update_author),
    path('admin/admin-upgrade/', views.upgrade_to_admin),
    path('admin/moderator-upgrade/', views.upgrade_to_moderator),
]