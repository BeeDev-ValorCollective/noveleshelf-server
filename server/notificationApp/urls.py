from django.urls import path
from . import views

# api/notifications/

urlpatterns = [
    # user endpoints
    path('my-notifications/', views.get_my_notifications),
    path('mark-read/', views.mark_notification_read),
    path('mark-all-read/', views.mark_all_read),
    path('clear/', views.clear_notifications),
    path('my-preferences/', views.get_my_preferences),
    path('my-preferences/update/', views.update_my_preference),

    # admin endpoints
    path('admin/types/', views.list_notification_types),
    path('admin/user-preferences/', views.get_user_preferences),
    path('admin/user-preferences/update/', views.update_user_preference),
    path('admin/user-permissions/update/', views.update_user_permission),
    path('admin/system-emails/', views.list_system_emails),
    path('admin/system-emails/create/', views.create_system_email),
    path('admin/system-emails/update/', views.update_system_email),
]