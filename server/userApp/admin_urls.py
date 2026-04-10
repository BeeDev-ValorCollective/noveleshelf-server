from django.urls import path
from .views import admin_views

urlpatterns = [
    path('author-upgrade/', admin_views.upgrade_to_author),
    path('admin-upgrade/', admin_views.upgrade_to_admin),
    path('moderator-upgrade/', admin_views.upgrade_to_moderator),
    path('author-update/', admin_views.admin_update_author),
    path('deactivate-user/', admin_views.deactivate_user),
    path('reactivate-user/', admin_views.reactivate_user),
]