from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


# Category Model
class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# Custom Manager (Published Only)
class PublishedBlogManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status="published")


# Blog Model
class Blog(models.Model):

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="blog_posts")

    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name="blogs")

    thumbnail = models.ImageField(upload_to="blog_thumbnails/",
                                  blank=True,
                                  null=True)

    # CKEditor 5 Field
    content = CKEditor5Field("Content", config_name="default")

    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default="draft",
                              db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedBlogManager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["status"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_published(self):
        return self.status == "published"


# Comment Model
class Comment(models.Model):

    blog = models.ForeignKey(Blog,
                             on_delete=models.CASCADE,
                             related_name="comments")

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="blog_comments")

    parent = models.ForeignKey("self",
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name="replies")

    content = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["is_approved"]),
        ]

    def save(self, *args, **kwargs):
        if self.parent and self.parent.parent is not None:
            raise ValueError(
                "Nested replies beyond one level are not allowed.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} on {self.blog.title}"

    @property
    def is_parent(self):
        return self.parent is None
