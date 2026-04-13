from django.urls import path
from .views import public_views

urlpatterns = [
    path('authors/', public_views.public_authors),
]