from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView, CreateView, ListView, FormView
from .models import Teacher, Tests
from django.urls import reverse_lazy
from SchoolSystem.views import WhichUserMixin
from students.models import Classes, Student
# Create your views here.
class TeacherUpdate(UpdateView):
    model = Teacher
    fields = ['subject', 'form_teacher', 'classes']
    template_name = 'update.html'
    success_url = reverse_lazy('home')


class TeacherDetails(WhichUserMixin, DetailView):
    template_name = 'teacher_detail.html'
    model = Teacher



class CreateTest(WhichUserMixin, CreateView):
    model = Tests
    fields = ['desc', 'classes']
    template_name = 'create_test.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        test = form.save(commit=False)
        teacher = Teacher.objects.get(user = self.request.user)
        class_name = form.cleaned_data['classes']
        desc =  form.cleaned_data['desc']
        classes = Classes.objects.get(name = class_name)
        students = classes.students.all()
        students_list = list(students)
        if len(students_list)>1:
            students = students_list.pop()
            print(students)
            for student in students_list:
                Tests.objects.create(desc=desc, teacher = teacher, classes = classes, student = student, subject = teacher.subject )
                print('test created for: ' + student.user.username)
        test.teacher = teacher
        test.subject = teacher.subject
        test.student = students
        print('test created for: ' + test.student.user.username)
        return super(CreateTest, self).form_valid(form)

class GradingSystem(WhichUserMixin, UpdateView):
    model = Tests
    fields = ['grades']
    template_name = 'grade_tests.html'
    success_url = reverse_lazy('home')

class TestDetails(WhichUserMixin, DetailView):
    model = Tests
    template_name = 'tests_details.html'

class TestUpdate(UpdateView):
    model = Tests
    fields = ['grade']
    template_name = "tests_update.html"
    success_url = reverse_lazy('home')

from django import forms
from django.db import models
SUBJECTS = ((1, "F"), (2,"E"), (3,"D"), (4, "C"), (5,"B"), (6,"A"))
class GradeForm(forms.Form):
    model = Tests
    grade = forms.ChoiceField(choices = SUBJECTS)

from django.http import HttpResponse


class ClassDetails(WhichUserMixin, DetailView):
    model = Classes
    template_name = "class_test_details.html"
    success_url = reverse_lazy('home')
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        tests = Tests.objects.all().filter(grade = None, teacher = self.current_teacher)
        context['ungraded_tests'] = tests
        context['form'] = GradeForm()
        return context

    def post(self, request,*args, **kwargs):
        teachers = Teacher.objects.all()
        students = Student.objects.all()
        teacher_list = []
        students_list = []
        for teacher in teachers:
            teacher_list.append(teacher.user.username)
        for student in students:
            students_list.append(student.user.username)
        if self.request.user.is_authenticated and self.request.user.username in teacher_list:
            self.current_teacher = Teacher.objects.get(user = self.request.user)
            self.current_student = None
        test = Tests.objects.all().filter(grade = None, teacher = self.current_teacher).first()

        form = GradeForm(request.POST)
        if form.is_valid():
            form =  form.cleaned_data['grade']
            test.grade = int(form)
            test.save()

        return HttpResponse("Here's the text of the Web page.")
