from django.db import models
from django.contrib.auth.models import User
from students.models import Classes, Student
# Create your models here.
SUBJECTS = (('En', 'English'), ('M','Maths'), ('PE','PE'), ('His','History'), ('Bio','Biology'), ('Ph','Physics'))

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher = models.BooleanField(default=False)
    subject = models.CharField(max_length=10, choices=SUBJECTS)
    form_teacher = models.CharField(max_length = 5, blank = True ,default = False)
    classes = models.ManyToManyField(Classes, related_name='teacher_classes')

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Tests(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE, null = True)
    desc = models.CharField(max_length = 50, null = True)
    student = models.ForeignKey(Student, on_delete = models.CASCADE, null = True)
    subject = models.CharField(max_length=10, choices=SUBJECTS, null = True)
    classes = models.ForeignKey(Classes, on_delete = models.CASCADE, null = True)
    class Grades(models.IntegerChoices):
        F = 1
        E = 2
        D = 3
        C = 4
        B = 5
        A = 6

    grade = models.IntegerField(choices = Grades.choices, null = True)
    def __str__(self):
        return self.desc 
