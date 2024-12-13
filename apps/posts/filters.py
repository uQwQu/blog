import django_filters

from .models import Post


class PostFilter(django_filters.FilterSet):
    author_username = django_filters.CharFilter(
        field_name="author__username", lookup_expr="icontains"
    )
    ordering = django_filters.OrderingFilter(
        fields=(
            ("created_at", "oldest"),
            ("-created_at", "most_recent"),
        )
    )

    class Meta:
        model = Post
        fields = ["author_username", "ordering", ]
