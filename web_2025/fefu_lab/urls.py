from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<slug:slug>/', views.course_detail, name='course_detail'),
    path('enrollment/', views.enrollment_view, name='enrollment'),
    path('enrollment/success/', views.enrollment_success, name='enrollment_success'),
    path('register/', views.register_student, name='register_student'),
    path('feedback/', views.feedback_view, name='feedback'),
]
