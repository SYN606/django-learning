from django.urls import path
from . import views

app_name = 'device_details'

urlpatterns = [
    path('', views.index, name='dev_details')
]
