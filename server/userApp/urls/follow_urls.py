from django.urls import path
from userApp.views.follow_views import MyFollowingView, UnfollowView

# api/follow/

urlpatterns = [
    path('reader/following/', MyFollowingView.as_view(), name='my-following'),
    path('reader/following/<int:follow_id>/', UnfollowView.as_view(), name='unfollow'),
]