from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Comment, Follow, Post, PostLike, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "is_published",
        "thumbnail",
        "created_at",
    )
    list_filter = ("is_published", "category", "created_at")
    search_fields = ("title", "excerpt", "content", "author__username")
    filter_horizontal = ("tags",)
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at", "updated_at", "thumbnail_large")
    inlines = (CommentInline,)
    autocomplete_fields = ("author", "category")

    fieldsets = (
        (None, {"fields": ("title", "slug", "author", "is_published")}),
        ("Content", {"fields": ("excerpt", "content", "cover_image", "thumbnail_large")}),
        ("Taxonomy", {"fields": ("category", "tags")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    @admin.display(description="Cover")
    def thumbnail(self, obj: Post):
        if obj.cover_image:
            return format_html(
                '<img src="{}" width="60" height="40" style="object-fit:cover;" />',
                obj.cover_image.url,
            )
        return "—"

    @admin.display(description="Cover preview")
    def thumbnail_large(self, obj: Post):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-width:320px;max-height:200px;" />',
                obj.cover_image.url,
            )
        return "No image"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "snippet", "created_at")
    list_filter = ("created_at",)
    search_fields = ("body", "author__username", "post__title")
    autocomplete_fields = ("post", "author")

    @admin.display(description="Body")
    def snippet(self, obj: Comment):
        return obj.body[:60] + ("…" if len(obj.body) > 60 else "")


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")
    autocomplete_fields = ("post", "user")


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("follower", "following", "created_at")
    autocomplete_fields = ("follower", "following")
