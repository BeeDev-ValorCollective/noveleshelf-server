from django.urls import path
from booksApp.views import admin_views

urlpatterns = [
    path('genres/', admin_views.list_genres),
    path('genres/create/', admin_views.create_genre),
    path('genres/update/', admin_views.update_genre),
    path('content-ratings/', admin_views.list_content_ratings),
    path('content-ratings/create/', admin_views.create_content_rating),
    path('content-ratings/update/', admin_views.update_content_rating),
    path('relationship-tags/', admin_views.list_relationship_tags),
    path('relationship-tags/create/', admin_views.create_relationship_tag),
    path('relationship-tags/update/', admin_views.update_relationship_tag),
    path('keywords/', admin_views.list_keywords),
    path('keywords/create/', admin_views.create_keyword),
    path('keywords/update/', admin_views.update_keyword),
]