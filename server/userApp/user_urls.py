from django.urls import path
from .views import user_views

urlpatterns = [
    path('profile/update/', user_views.update_profile),
    path('default-role/update/', user_views.update_default_role),
    path('author-profile/update/', user_views.update_author_profile),
    path('admin-profile/update/', user_views.update_admin_profile),
    path('moderator-profile/update/', user_views.update_moderator_profile),
    path('change-password/', user_views.change_password),
    path('change-email/', user_views.change_email),
]