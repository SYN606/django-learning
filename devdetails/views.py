from django.shortcuts import render
from .models import Students


def index(request):
    student_data = Students.objects.all()  # select * from Students
    data = {'student_data': student_data}
    return render(request, 'dev_details.html', data)


def detailed_view(request, pk):
    student = Students.objects.get(pk=pk)  
    data = {'student': student}
    return render(request, 'details.html', data)


