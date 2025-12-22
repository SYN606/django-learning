import uuid
from django.db import models
from django.core.validators import RegexValidator


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    id_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z0-9]+$',
                message="ID must contain only uppercase letters and numbers.")
        ])

    role = models.CharField(max_length=50,
                            choices=[
                                ("student", "Student"),
                                ("cr", "Class Representative"),
                                ("admin", "Admin"),
                            ],
                            default="student")

    about = models.TextField(blank=True)

    # Image field
    profile_image = models.ImageField(upload_to="students/profile_images/",
                                      blank=True,
                                      null=True)

    is_active = models.BooleanField(default=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id_number"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.id_number})"
