from django.shortcuts import render
from .models import Students


def index(request):
    student_data = Students.objects.all()  # select * from Students
    return render(request, 'dev_details.html')
