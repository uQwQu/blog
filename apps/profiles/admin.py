from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "pkid", "user", "private", "country"]
    list_filter = ["private", "country"]
    list_display_links = ["id", "pkid", "user"]
    readonly_fields = ("user",)


admin.site.register(Profile, ProfileAdmin)
