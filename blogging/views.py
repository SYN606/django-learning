from django.shortcuts import render
from .models import Blog


def blogpage(request):
    b = Blog.objects.all()
    print(b)
    data = {'blogs': b}
    return render(request, 'blog_homepage.html', data)
