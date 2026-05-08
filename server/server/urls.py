from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.api_root),
    path('api/debug/health/', views.health_check),
    path('api/debug/test-email/', views.test_email),
    path('api/debug/login/', views.debug_login),
    path('api/debug/me/', views.debug_me),
    path('api/public/', include('userApp.urls.public_urls')),
    path('api/auth/', include('userApp.urls.auth_urls')),
    path('api/user/', include('userApp.urls.user_urls')),
    path('api/admin/users/', include('userApp.urls.admin_urls')),
    path('api/notifications/', include('notificationApp.urls')),
    path('api/books/admin/', include('booksApp.urls.admin_urls')),
    path('api/books/author/', include('booksApp.urls.author_urls')),
    path('api/books/public/', include('booksApp.urls.public_urls')),
    path('api/books/user/', include('booksApp.urls.user_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)