from django.urls import path
from booksApp.views import author_views

urlpatterns = [
    path('books/create/', author_views.create_book),
    path('books/', author_views.list_my_books),
    path('books/update/', author_views.update_book),
    path('books/submit/', author_views.submit_book),
    path('books/delete/', author_views.delete_book),
    path('books/genres/add/', author_views.add_genre),
    path('books/genres/remove/', author_views.remove_genre),
    path('books/relationship-tags/add/', author_views.add_relationship_tag),
    path('books/relationship-tags/remove/', author_views.remove_relationship_tag),
    path('books/keywords/add/', author_views.add_keyword),
    path('books/keywords/remove/', author_views.remove_keyword),
]