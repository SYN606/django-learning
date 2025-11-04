from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages


def homepage(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)  
            messages.success(request, f'Welcome back, {user.username}!')

        return redirect('homepage')
    else :
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')

        name = name.split(' ')
        *first_name, last_name = name
        first_name = ' '.join(map(str, first_name))
        
        user = User(first_name=first_name, last_name=last_name, email=email, password=password, username=username)

        user.save()

        return redirect('login')
    else:
        return render(request, 'register.html')
    
def logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')