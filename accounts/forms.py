from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)
    #extra form fields
    teacher = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
        ]
