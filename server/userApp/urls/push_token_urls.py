from django.urls import path

from userApp.views.push_token_views import (
    PushTokenView,
)


urlpatterns = [
    path(
        '',
        PushTokenView.as_view(),
        name='push-token'
    ),
]