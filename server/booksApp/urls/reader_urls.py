from django.urls import path
from booksApp.views.reader_views import (
    MyLibraryView, MyLibraryBookView,
    ChapterReadView, ChapterUnlockView,
)

urlpatterns = [
    # Reader - Library
    path('library/', MyLibraryView.as_view(), name='my-library'),
    path('library/<int:book_id>/', MyLibraryBookView.as_view(), name='my-library-book'),

    # Reader - Chapters
    path('chapters/<int:chapter_id>/read/', ChapterReadView.as_view(), name='chapter-read'),
    path('chapters/<int:chapter_id>/unlock/', ChapterUnlockView.as_view(), name='chapter-unlock'),
]