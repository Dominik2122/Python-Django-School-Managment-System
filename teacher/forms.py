from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Tests
from students.models import Classes
from django.contrib.admin import widgets
classes = Classes.objects.all()
classes = list(classes)
CLASSES = []
for clas in classes:
    CLASSES.append((clas , clas.name))


SUBJECTS = ((1, "F"), (2,"E"), (3,"D"), (4, "C"), (5,"B"), (6,"A"))
class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
        ]

class TestForm(forms.ModelForm):
    class Meta:
        model = Tests
        fields = ('desc', 'classes','planned')
