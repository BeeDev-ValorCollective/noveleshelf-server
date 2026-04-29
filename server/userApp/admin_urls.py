from django.urls import path
from .views import admin_views

urlpatterns = [
    path('author-upgrade/', admin_views.upgrade_to_author),
    path('admin-upgrade/', admin_views.upgrade_to_admin),
    path('moderator-upgrade/', admin_views.upgrade_to_moderator),
    path('author-update/', admin_views.admin_update_author),
    path('free-author/update/', admin_views.admin_update_free_author),
    path('deactivate-user/', admin_views.deactivate_user),
    path('reactivate-user/', admin_views.reactivate_user),
    path('list/', admin_views.list_users),
    path('author-requests/', admin_views.list_author_requests),
    path('author-request/update/', admin_views.update_author_request),
    path('author-request/approve/', admin_views.approve_author_request),
    path('deactivate-author/', admin_views.deactivate_author),
    path('reactivate-author/', admin_views.reactivate_author),
]