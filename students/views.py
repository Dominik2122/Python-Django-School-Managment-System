from django.shortcuts import render
from .models import Student, Classes
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView, ListView, TemplateView
from teacher.models import Teacher, Tests
from django.urls import reverse_lazy
from SchoolSystem.views import WhichUserMixin

# Create your views here.

class StudentsDetails(WhichUserMixin, DetailView):
    model = Student
    template_name = 'details.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subjects = ['English','Maths','PE','History','Biology','Physics']
        context['subjects']=subjects
        means_list = []
        for subject in subjects:
            tests = Tests.objects.filter(grade__isnull=False, subject = subject, student = self.current_student)
            mean = 0
            i = 0
            for test in tests:
                i += 1
                mean += int(test.grade)
            if i != 0:
                num = mean/i
                mean = ["{:.2f}".format(num), subject]
            else:
                mean = ['None', subject]
            means_list.append(mean)
        context['means_list']= means_list
        classes = Classes.objects.filter(students = self.current_student).first().name
        context['class']= classes
        return context

class StudentsGrades(WhichUserMixin, TemplateView):
    template_name = 'grades.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tests = Tests.objects.filter(grade__isnull=False, subject = self.subject, student = self.current_student)
        context['subject'] = self.subject
        context['tests'] = list(tests)
        mean = 0
        i = 0
        for test in tests:
            i += 1
            mean += int(test.grade)
        if i != 0:
            num = mean/i
            mean = "{:.2f}".format(num)
        else:
            mean = 'None'
        context['mean'] = mean
        context['subjects'] =['English','Maths','PE','History','Biology','Physics']
        return context
    def get(self,request,*args,**kwargs):
        self.subject = request.get_full_path()[17:-1]
        return super().get(request, *args, **kwargs)
