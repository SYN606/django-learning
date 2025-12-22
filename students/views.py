from django.shortcuts import render, get_object_or_404
from .models import Student


def index(request):
    students = Student.objects.filter(is_active=True)
    context = {"students": students}
    return render(request, "std-details.html", context)


def detailed_view(request, pk):
    student = get_object_or_404(Student, pk=pk, is_active=True)
    context = {"student": student}
    return render(request, "details.html", context)
