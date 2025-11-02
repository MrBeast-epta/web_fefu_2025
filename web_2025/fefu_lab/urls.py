from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('student/<int:student_id>/', views.StudentProfileView.as_view(), name='student_profile'),
    path('course/<slug:course_slug>/', views.course_detail, name='course_detail'),
]
