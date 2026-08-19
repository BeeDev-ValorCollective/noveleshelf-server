from django.urls import path
from userApp.views.follow_views import MyFollowingView, UnfollowView, FollowStatusView

# api/follow/

urlpatterns = [
    path('reader/following/', MyFollowingView.as_view(), name='my-following'),
    path('reader/following/<int:follow_id>/', UnfollowView.as_view(), name='unfollow'),
    path('reader/following/status/<str:profile_type>/<int:profile_id>/', FollowStatusView.as_view(), name='follow-status'),
]