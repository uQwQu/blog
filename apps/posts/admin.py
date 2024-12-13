from django.contrib import admin

from .models import Post, PostImage


class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "author",
        "title",
        "slug",
    ]
    list_filter = [
        "author",
    ]
    readonly_fields = ("slug",)


class PostImageAdmin(admin.ModelAdmin):
    list_display = ["image", "post", "author"]
    search_fields = ["post__title", "post__slug", "post__author__email"]


admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
