from django.db.models import Q

from apps.posts.models import Post


def get_posts(user):
    return Post.objects.filter(Q(author__profile__private=False) | Q(author=user))


def get_bookmarked_posts(user):
    return Post.objects.filter(
        Q(author__profile__private=False) | Q(author=user), bookmarked_by=user
    )
