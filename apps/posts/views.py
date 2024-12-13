import logging

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.posts.filters import PostFilter
from apps.posts.models import Post
from apps.posts.permissions import IsOwnerOrReadOnly
from apps.posts.post_access import get_bookmarked_posts, get_posts
from apps.posts.serializers import PostSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_posts(self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        logger.info(
            f"Post '{instance.title}' created by {self.request.user.first_name}"
        )


class MyPostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by(
            "-upvotes", "-created_at"
        )


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        return get_posts(self.request.user)


@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def bookmark_post_api_view(request, slug):
    user = request.user
    accessible_post = get_posts(user)
    post = get_object_or_404(accessible_post, slug=slug)

    if user in post.bookmarked_by.all():
        return Response(
            {"message": "Post already bookmarked"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    post.bookmarked_by.add(user)
    return Response({"message": "Post bookmarked"}, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def unbookmark_post_api_view(request, slug):
    user = request.user
    accessible_post = get_posts(user)
    post = get_object_or_404(accessible_post, slug=slug)

    if user not in post.bookmarked_by.all():
        return Response(
            {"message": "You can't remove a bookmark that did not exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    post.bookmarked_by.remove(user)
    return Response({"message": "Post Bookmark Removed"}, status=status.HTTP_200_OK)


class BookmarkedPostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_bookmarked_posts(self.request.user)
