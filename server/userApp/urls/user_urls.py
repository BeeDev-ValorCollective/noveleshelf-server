from django.urls import path
from userApp.views import user_views

# api/user/

urlpatterns = [
    path('profile/update/', user_views.update_profile),
    path('default-role/update/', user_views.update_default_role),
    path('author-profile/update/', user_views.update_author_profile),
    path('admin-profile/update/', user_views.update_admin_profile),
    path('moderator-profile/update/', user_views.update_moderator_profile),
    path('change-password/', user_views.change_password),
    path('change-email/', user_views.change_email),
    path('free-author/upgrade/', user_views.upgrade_to_free_author),
    path('free-author-profile/update/', user_views.update_free_author_profile),
    path('author-request/submit/', user_views.submit_author_request),
    path('author-request/my-requests/', user_views.get_my_author_requests),
    path('author-dashboard/', user_views.author_dashboard),
    path('free-author-dashboard/', user_views.free_author_dashboard),
]