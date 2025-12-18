from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as user_logout
from django.contrib import messages


def homepage(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request,
                             f"Hello, {username}, Welcome to HackersvellA.")
            return redirect('home:homepage')
        else:
            messages.error(request, "Username and password did not match.")
            return render(request, 'login.html')

    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            passwd = request.POST.get('password')
            fname = request.POST.get('first_name')
            lname = request.POST.get('last_name')

            # Validate BEFORE creating user
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return render(request, 'register.html')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return render(request, 'register.html')

            # Single DB write
            User.objects.create_user(username=username,
                                     email=email,
                                     password=passwd,
                                     first_name=fname,
                                     last_name=lname)

            messages.success(request,
                             "Account created successfully. Please log in.")
            return redirect('home:login')

        except Exception:
            messages.error(request, "Something went wrong. Please try again.")
            return render(request, 'register.html')

    return render(request, 'register.html')


def logout(request):
    user_logout(request)
    messages.info(request, "User logged out successfully")
    return redirect('home:homepage')
