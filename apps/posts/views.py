import logging

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.posts.filters import PostFilter
from apps.posts.models import Post
from apps.posts.permissions import IsOwnerOrReadOnly
from apps.posts.post_access import get_bookmarked_posts, get_posts
from apps.posts.serializers import PostSerializer, UpvotePostSerializer, DownvotePostSerializer

User = get_user_model()

logger = logging.getLogger(__name__)


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    filterset_class = PostFilter
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return get_posts(self.request.user)


class MyPostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    filterset_class = PostFilter

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by(
            "-upvotes", "-created_at"
        )


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        logger.info(
            f"Post '{instance.title}' created by {self.request.user.first_name}"
        )


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        return get_posts(self.request.user)


@api_view(["PATCH"])
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

    def get_queryset(self):
        return get_bookmarked_posts(self.request.user)


@api_view(["PATCH"])
def upvote_post_api_view(request, slug):
    user = request.user
    accessible_post = get_posts(user)
    post = get_object_or_404(accessible_post, slug=slug)
    serializer = UpvotePostSerializer(
        post, data=request.data, context={"request": request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Post upvoted successfully!"}, status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
def downvote_post_api_view(request, slug):
    user = request.user
    accessible_post = get_posts(user)
    post = get_object_or_404(accessible_post, slug=slug)
    serializer = DownvotePostSerializer(post, data={}, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "Post downvoted successfully!"}, status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
