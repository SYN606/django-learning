from django.db import transaction, IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


# Homepage
def homepage(request):
    return render(request, "index.html")


# Register
def register_view(request):
    if request.user.is_authenticated:
        return redirect("home:homepage")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, "register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "register.html")

        try:
            validate_password(password)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, "register.html")

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    is_active=True,
                    is_verified=True)  # pyright: ignore[reportCallIssue]

        except IntegrityError:
            messages.error(request, "Something went wrong. Please try again.")
            return render(request, "register.html")

        except Exception:
            messages.error(request, "Unexpected error occurred.")
            return render(request, "register.html")

        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("home:homepage")

    return render(request, "register.html")


# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect("homepage")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            next_url = request.GET.get("next")
            return redirect(next_url if next_url else "home:homepage")

        messages.error(request, "Invalid email or password.")
        return render(request, "login.html")

    return render(request, "login.html")


# Logout
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("home:homepage")


# About Page
def about_view(request):
    return render(request, "about.html")
