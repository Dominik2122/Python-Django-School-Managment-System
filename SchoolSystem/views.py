from django.views.generic import TemplateView
from teacher.models import Teacher, Tests
from students.models import Student
from django.contrib.auth import get_user_model
current_user = get_user_model()


class WhichUserMixin:
    def get(self, request, *args, **kwargs):
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
        elif self.request.user.is_authenticated and self.request.user.username in students_list:
            self.current_teacher = None
            self.current_student = Student.objects.get(user = self.request.user)
        else:
            self.current_teacher = None
            self.current_student = None
        return super().get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_teacher'] = self.current_teacher
        context['current_student'] = self.current_student
        return context


class HomePage(WhichUserMixin, TemplateView):
    def get_template_names(self):
        if self.current_teacher:
            return ['teacher_index.html']
        elif self.current_student:
            return['student_index.html']
        else:
            return ['index.html']
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        tests = Tests.objects.filter(grade = None, teacher = self.current_teacher)
        ungraded_tests = tests.values_list('classes', 'desc')
        list(ungraded_tests)
        ungraded_tests_classes = []
        for tup in ungraded_tests:
            if tup not in ungraded_tests_classes:
                ungraded_tests_classes.append(tup)
        ungraded_tests = []
        for tup in ungraded_tests_classes:
            ungraded_tests.append(Tests.objects.filter(grade = None, teacher = self.current_teacher, classes = tup[0], desc = tup[1]).first())
        context['ungraded_tests'] = ungraded_tests
        return context
    
