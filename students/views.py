from django.shortcuts import render
from .models import Student, Classes
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView, ListView
from teacher.models import Teacher, Tests
from django.urls import reverse_lazy
from SchoolSystem.views import WhichUserMixin

# Create your views here.

class StudentsDetails(WhichUserMixin, DetailView):
    model = Student
    template_name = 'details.html'

class StudentsGrades(WhichUserMixin, ListView):
    model = Tests
    template_name = 'student_index.html'
    def get_queryset(self):
        qs = super().get_queryset()
        print('heloo')
        return qs.all()
