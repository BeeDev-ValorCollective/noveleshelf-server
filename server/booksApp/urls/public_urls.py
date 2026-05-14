from django.urls import path
from booksApp.views import public_views

urlpatterns = [
    path('featured/', public_views.featured),
    path('books/', public_views.book_list),
    path('books/<int:book_id>/', public_views.book_detail),
]