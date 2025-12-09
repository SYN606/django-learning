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
            return redirect('homepage')
        else:
            messages.error(request, "Username and password did not match.")
            return render(request, 'login.html')

    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        passwd = request.POST.get('password')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')

        User.objects.create_user(username=username,
                                 email=email,
                                 password=passwd,
                                 first_name=fname,
                                 last_name=lname)

        messages.success(request,
                         "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'register.html')


def logout(request):
    user_logout(request)
    messages.info(request, "User logged out successfully")
    return redirect('homepage')
