from django.urls import path

from apps.profiles.views import (
    MyProfileDetailAPIView,
    ProfileDetailAPIView,
    ProfileListAPIView,
    ProfileUpdateAPIView,
    avatar_upload_api_view,
)

urlpatterns = [
    path("me/", MyProfileDetailAPIView.as_view(), name="profile-me"),
    path("update/", ProfileUpdateAPIView.as_view(), name="profile-update"),
    path("avatar/", avatar_upload_api_view, name="avatar-upload"),
    path("all/", ProfileListAPIView.as_view(), name="profile-all"),
    path("<str:username>/", ProfileDetailAPIView.as_view(), name="profile-sb"),
]
