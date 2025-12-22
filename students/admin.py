from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Columns shown in list view
    list_display = (
        "name",
        "id_number",
        "role",
        "is_active",
        "created_at",
    )

    list_display_links = ("name", "id_number")

    list_filter = ("role", "is_active", "created_at")

    search_fields = ("name", "id_number")

    ordering = ("name", )

    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "id_number", "role", "about")
        }),
        ("Profile", {
            "fields": ("profile_image", ),
        }),
        ("Status & Metadata", {
            "fields": ("is_active", "id", "created_at", "updated_at"),
        }),
    )
