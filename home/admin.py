from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ("email", "is_staff", "is_verified")
    ordering = ("email", )

    fieldsets = (
        (None, {
            "fields": ("email", "password")
        }),
        ("Permissions", {
            "fields": ("is_staff", "is_superuser", "is_verified", "groups",
                       "user_permissions")
        }),
        ("Important dates", {
            "fields": ("last_login", )
        }),
    )

    add_fieldsets = ((None, {
        "classes": ("wide", ),
        "fields":
        ("email", "password1", "password2", "is_staff", "is_superuser"),
    }), )
