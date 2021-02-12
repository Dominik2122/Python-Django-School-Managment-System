from django.shortcuts import render
from .models import Student, Classes
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
from teacher.models import Teacher
from django.urls import reverse_lazy
from SchoolSystem.views import WhichUserMixin

# Create your views here.

class StudentsDetails(WhichUserMixin, DetailView):
    model = Student
    template_name = 'details.html'
