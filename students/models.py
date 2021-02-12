from django.db import models
from django.contrib.auth.models import User

# Create your models here.
SUBJECTS = (('En', 'English'), ('M','Maths'), ('PE','PE'), ('His','History'), ('Bio','Biology'), ('Ph','Physics'))

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Classes(models.Model):
    name = models.CharField(max_length = 5)
    students = models.ManyToManyField(Student)
    def __str__(self):
        return self.name
