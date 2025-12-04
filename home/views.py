from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def homepage(request):
    return render(request, 'index.html')


def login(request):

    if request.method == 'POST':
        print("HELLLO")
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        passwd = request.POST.get('password')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')

        user = User(username=username,
                    email=email,
                    password=passwd,
                    first_name=fname,
                    last_name=lname)
        user.save()
        return redirect('login')
    else:
        return render(request, 'register.html')
