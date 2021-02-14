from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'teacher'
urlpatterns = [
    path('update/<int:pk>/', views.TeacherUpdate.as_view(), name = 'update'),
    path('detail/<int:pk>/', views.TeacherDetails.as_view(), name = 'detail'),
    path('create/test/', views.CreateTest.as_view(), name = 'test_create'),
    path('tests/details/<int:pk>/', views.TestDetails.as_view(), name = 'test_details'),
    path("class/<int:pk>", views.ClassDetails.as_view(), name  = 'class'),
]
