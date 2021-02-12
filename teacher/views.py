from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView, CreateView
from .models import Teacher, Tests
from django.urls import reverse_lazy
from SchoolSystem.views import WhichUserMixin
from students.models import Classes
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
            for student in students_list:
                Tests.objects.create(desc=desc, teacher = teacher, classes = classes, student = student, subject = teacher.subject )
        test.teacher = teacher
        test.subject = teacher.subject
        test.student = students_list[0]
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
    template_name = 'tests_update.html'
    success_url = reverse_lazy('home')
