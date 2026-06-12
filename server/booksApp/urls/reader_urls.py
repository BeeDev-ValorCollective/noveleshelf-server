from django.urls import path
from booksApp.views.reader_views import (
    MyLibraryView, MyLibraryBookView,
    ChapterReadView, ChapterUnlockView,
)

urlpatterns = [
    # Reader - Library
    path('reader/library/', MyLibraryView.as_view(), name='my-library'),
    path('reader/library/<int:book_id>/', MyLibraryBookView.as_view(), name='my-library-book'),

    # Reader - Chapters
    path('reader/chapters/<int:chapter_id>/read/', ChapterReadView.as_view(), name='chapter-read'),
    path('reader/chapters/<int:chapter_id>/unlock/', ChapterUnlockView.as_view(), name='chapter-unlock'),
]