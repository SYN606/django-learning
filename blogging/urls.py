from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.blogpage, name='blog_page'), 
]
