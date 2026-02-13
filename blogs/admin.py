from django.contrib import admin
from .models import Blog, Category, Comment


# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name", )
    prepopulated_fields = {"slug": ("name", )}
    readonly_fields = ("created_at", )
    ordering = ("name", )


# Comment Inline (For Blog Admin)
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ("user", "content", "is_approved", "created_at")
    readonly_fields = ("created_at", )
    show_change_link = True


# Blog Admin
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "status",
        "created_at",
        "updated_at",
    )

    list_filter = ("status", "category", "created_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title", )}
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("status", )
    date_hierarchy = "created_at"
    ordering = ("-created_at", )
    inlines = [CommentInline]


# Comment Admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "blog",
        "parent",
        "is_approved",
        "created_at",
    )

    list_filter = ("is_approved", "created_at")
    search_fields = ("content", "user__email", "blog__title")
    readonly_fields = ("created_at", )
    ordering = ("-created_at", )
