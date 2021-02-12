from django.contrib import admin

# Register your models here.
from .models import Student, Classes
# Register your models here.

admin.site.register(Student)
admin.site.register(Classes)
