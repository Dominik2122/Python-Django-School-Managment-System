from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView, CreateView, ListView, FormView
from .models import Teacher, Tests
from django.urls import reverse_lazy
from SchoolSystem.views import WhichUserMixin
from students.models import Classes, Student
from django import forms
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
class TeacherUpdate(UpdateView):
    model = Teacher
    fields = ['subject', 'form_teacher', 'classes']
    template_name = 'update.html'
    success_url = reverse_lazy('home')


class TeacherDetails(WhichUserMixin, DetailView):
    template_name = 'teacher_detail.html'
    model = Teacher
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        classes = list(self.current_teacher.classes.all())
        context['classes'] = classes
        tests = Tests.objects.filter(grade__isnull = False, teacher = self.current_teacher)
        graded_tests = tests.values_list('classes', 'desc')
        list(graded_tests)
        graded_tests_classes = []
        for tup in graded_tests:
            if tup not in graded_tests_classes:
                graded_tests_classes.append(tup)
        graded_tests = []
        for tup in graded_tests_classes:
            graded_tests.append(Tests.objects.filter(grade__isnull = False, teacher = self.current_teacher, classes = tup[0], desc = tup[1]).first())
        context['tests'] = graded_tests[:6]
        return context

class TestForm(forms.ModelForm):
    class Meta:
        model = Tests
        fields = ['desc', 'classes', 'planned']
        labels = {
        "desc": 'Description',
        'classes': "Class",
        'planned': "Date [Y-M-D]"
    }


class CreateTest(WhichUserMixin, CreateView):
    model = Tests
    form_class = TestForm
    template_name = 'create_test.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        test = form.save(commit=False)
        teacher = Teacher.objects.get(user = self.request.user)
        class_name = form.cleaned_data['classes']
        desc =  form.cleaned_data['desc']
        planned = form.cleaned_data['planned']
        classes = Classes.objects.get(name = class_name)
        students = classes.students.all()
        students_list = list(students)
        if len(students_list)>1:
            students = students_list.pop()
            print(students)
            for student in students_list:
                Tests.objects.create(desc=desc, teacher = teacher, classes = classes, student = student, subject = teacher.subject, planned = planned )
                print('test created for: ' + student.user.username)
        test.teacher = teacher
        test.subject = teacher.subject
        test.planned = planned
        test.student = students.first()
        print('test created for: ' + test.student.user.username)
        return super(CreateTest, self).form_valid(form)


class ClassDetails(WhichUserMixin, DetailView):
    model = Classes
    template_name = 'class_details.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        students = list(self.get_object().students.all())
        context['students'] = students
        students_tests = Tests.objects.all().filter(teacher = self.current_teacher, classes = self.get_object(), grade__isnull = False)
        context['students_tests'] = students_tests
        means_list = []
        for student in students:
            student_tests = list(students_tests.filter(student = student))
            mean = 0
            i = 0
            for test in student_tests:
                i += 1
                mean += int(test.grade)
            if i != 0:
                num = mean/i
                mean = "{:.2f}".format(num)
                mean = [mean, student]
            else:
                mean = ['None', student]
            means_list.append(mean)
        context['means_list'] = means_list
        return context





SUBJECTS = ((1, "F"), (2,"E"), (3,"D"), (4, "C"), (5,"B"), (6,"A"))

class GradeForm(forms.Form):
    model = Tests
    grade = forms.ChoiceField(choices = SUBJECTS)

class TestDetails(WhichUserMixin, DetailView):
    model = Tests
    template_name = "class_test_details.html"
    success_url = reverse_lazy('home')
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        tests = Tests.objects.all().filter(grade = None, classes = self.get_object().classes, desc = self.get_object().desc, teacher = self.current_teacher)
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
        test = Tests.objects.all().filter(grade = None, teacher = self.current_teacher,  desc = self.get_object().desc,  classes = self.get_object().classes)
        grades = request.POST.getlist('grade')
        i = 0

        for test_l in list(test):
            for element in SUBJECTS:
                if int(element[0]) == int(grades[i]):
                    print(element[0])
                    test_l.grade = int(element[0])
                    test_l.save()
            i += 1
        return HttpResponseRedirect(reverse_lazy('home'))
