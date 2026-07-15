from django.urls import path
from booksApp.views.reader_views import (
    my_library, my_library_remove_book, my_library_book_detail,
    chapter_read, chapter_unlock, set_auto_unlock_preference
)

# api/books/reader/

urlpatterns = [
    # Reader - Library
    path('library/', my_library, name='my-library'),
    path('library/<int:book_id>/', my_library_remove_book, name='my-library-remove-book'),
    path('library/book/<int:book_id>/', my_library_book_detail, name='my-library-book-detail'),
    path('library/book/<int:book_id>/auto-unlock/', set_auto_unlock_preference, name='set-auto-unlock-preference'),

    # Reader - Chapters
    path('chapters/<int:chapter_id>/read/', chapter_read, name='chapter-read'),
    path('chapters/<int:chapter_id>/unlock/', chapter_unlock, name='chapter-unlock'),
]