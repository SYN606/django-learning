from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about_view, name='about'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
