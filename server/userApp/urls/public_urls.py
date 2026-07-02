from django.urls import path
from userApp.views import public_views

urlpatterns = [
    path('authors/', public_views.public_authors),
    path('authors/<str:username>/', public_views.public_author_detail),
]