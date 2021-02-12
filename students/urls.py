from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'students'
urlpatterns = [
    path('detail/<int:pk>/', views.StudentsDetails.as_view(), name = 'detail'),
    ]
