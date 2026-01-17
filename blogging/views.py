from django.shortcuts import render

def blogpage(request):
    return render(request, 'blog_homepage.html')