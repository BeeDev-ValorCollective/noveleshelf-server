from django.urls import path
from booksApp.views import author_views

urlpatterns = [
    # Books
    path('books/create/', author_views.create_book),
    path('books/', author_views.list_my_books),
    path('books/update/', author_views.update_book),
    path('books/<int:book_id>/', author_views.get_book),
    path('books/submit/', author_views.submit_book),
    path('books/delete/', author_views.delete_book),
    path('books/genres/add/', author_views.add_genre),
    path('books/genres/remove/', author_views.remove_genre),
    path('books/relationship-tags/add/', author_views.add_relationship_tag),
    path('books/relationship-tags/remove/', author_views.remove_relationship_tag),
    path('books/keywords/add/', author_views.add_keyword),
    path('books/keywords/remove/', author_views.remove_keyword),

    # Chapters
    path('chapters/create/', author_views.create_chapter),
    path('chapters/', author_views.list_my_chapters),
    path('chapters/update/', author_views.update_chapter),
    path('chapters/publish/', author_views.publish_chapter),
    path('chapters/unpublish/', author_views.unpublish_chapter),
    path('chapters/delete/', author_views.delete_chapter),

    # Pages
    path('pages/create-update/', author_views.create_update_book_page),
    path('pages/publish/', author_views.publish_book_page),
    path('pages/unpublish/', author_views.unpublish_book_page),
    path('pages/delete/', author_views.delete_book_page),
]