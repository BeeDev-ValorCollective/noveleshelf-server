
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/debug/health/', views.health_check),
    path('api/debug/login/', views.debug_login),
    path('api/debug/me/', views.debug_me),
    path('api/auth/', include('userApp.urls')),
]
