from django.shortcuts import render
from django.urls import reverse_lazy
from . import forms
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from teacher.models import Teacher
from students.models import Student, Classes

class SignUp(CreateView):
    form_class = forms.CreateUserForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'signup.html'

    def form_valid(self, form):
        c = {'form' : form}
        user = form.save(commit=False)
        teacher = form.cleaned_data['teacher']
        password = form.cleaned_data['password']
        repeat_password = form.cleaned_data['repeat_password']
        if password != repeat_password:
            messages.error(self.request, "Passwords do not Match", extra_tags='alert alert-danger')
            return render(self.request, self.template_name, c)
        user.set_password(password)
        user.save()
        # Create Profile model
        if teacher == True:
            Teacher.objects.create(user=user, teacher=teacher)
        else:
            Student.objects.create(user=user)


        return super(SignUp, self).form_valid(form)
