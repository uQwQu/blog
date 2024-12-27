from django.urls import path

from apps.posts.views import (
    BookmarkedPostListAPIView,
    MyPostListAPIView,
    PostListAPIView,
    PostCreateAPIView,
    PostRetrieveUpdateDestroyAPIView,
    bookmark_post_api_view,
    unbookmark_post_api_view, upvote_post_api_view, downvote_post_api_view,
)

urlpatterns = [
    path("", PostListAPIView.as_view(), name="post-list"),
    path("my/", MyPostListAPIView.as_view(), name="post-my"),
    path("bookmarked/", BookmarkedPostListAPIView.as_view(), name="post-bookmarked"),
    path("create/", PostCreateAPIView.as_view(), name="post-create"),
    path(
        "<slug:slug>/",
        PostRetrieveUpdateDestroyAPIView.as_view(),
        name="post-retrieve-update-destroy",
    ),
    path("<slug:slug>/bookmark/", bookmark_post_api_view, name="post-bookmark"),
    path("<slug:slug>/unbookmark/", unbookmark_post_api_view, name="post-unbookmark"),
    path("<slug:slug>/upvote/", upvote_post_api_view, name="post-upvote"),
    path(
        "<slug:slug>/downvote/", downvote_post_api_view, name="post-downvote"),
]
