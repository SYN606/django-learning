from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Prefetch

from .models import Blog, Category, Comment


# Blog List View (With Pagination)
def blog_list_view(request):
    blog_queryset = (Blog.objects.filter(status="published").select_related(
        "author", "category").order_by("-created_at"))

    paginator = Paginator(blog_queryset, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog_list.html", {
        "blogs": page_obj,
        "page_obj": page_obj,
    })


# Category Filter View (With Pagination)
def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)

    blog_queryset = (Blog.objects.filter(
        category=category,
        status="published").select_related("author",
                                           "category").order_by("-created_at"))

    paginator = Paginator(blog_queryset, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog_list.html", {
        "blogs": page_obj,
        "page_obj": page_obj,
        "category": category,
    })


# Blog Detail View
def blog_detail_view(request, slug):
    blog = get_object_or_404(Blog.objects.select_related("author", "category"),
                             slug=slug,
                             status="published")

    comments = (blog.comments.filter( # type: ignore
        parent__isnull=True, is_approved=True).select_related("user").order_by(
            "-created_at").prefetch_related(
                Prefetch("replies",
                         queryset=Comment.objects.filter(is_approved=True).
                         select_related("user").order_by("created_at"))))

    total_comments = blog.comments.filter(is_approved=True).count() # type: ignore

    return render(request, "blog_detail.html", {
        "blog": blog,
        "comments": comments,
        "total_comments": total_comments,
    })


# Add Comment (Top-Level)
@login_required
def add_comment_view(request, slug):
    if request.method != "POST":
        return redirect("blogs:detail", slug=slug)

    blog = get_object_or_404(Blog, slug=slug, status="published")
    content = request.POST.get("content", "").strip()

    if not content:
        messages.error(request, "Comment cannot be empty.")
        return redirect("blogs:detail", slug=slug)

    with transaction.atomic():
        Comment.objects.create(blog=blog,
                               user=request.user,
                               content=content,
                               parent=None)

    messages.success(request, "Comment added successfully.")
    return redirect("blogs:detail", slug=slug)


# Add Reply (Threaded Reply)
@login_required
def add_reply_view(request, slug, comment_id):
    if request.method != "POST":
        return redirect("blogs:detail", slug=slug)

    blog = get_object_or_404(Blog, slug=slug, status="published")

    parent_comment = get_object_or_404(
        Comment,
        id=comment_id,
        blog=blog,
        is_approved=True,
        parent__isnull=True  # prevents reply-to-reply nesting
    )

    content = request.POST.get("content", "").strip()

    if not content:
        messages.error(request, "Reply cannot be empty.")
        return redirect("blogs:detail", slug=slug)

    with transaction.atomic():
        Comment.objects.create(blog=blog,
                               user=request.user,
                               content=content,
                               parent=parent_comment)

    messages.success(request, "Reply added successfully.")
    return redirect("blogs:detail", slug=slug)
