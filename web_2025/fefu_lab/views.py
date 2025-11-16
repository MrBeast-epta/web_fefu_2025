from django.shortcuts import render, get_object_or_404, redirect
from django.db import IntegrityError
from .models import Student, Course, Enrollment, Instructor
from .forms import StudentForm, EnrollmentForm

def home_page(request):
    total_students = Student.objects.count()
    total_courses = Course.objects.filter(is_active=True).count()
    total_instructors = Instructor.objects.count()
    recent_courses = Course.objects.filter(is_active=True).order_by('-created_at')[:3]
    
    return render(request, 'fefu_lab/home.html', {
        'title': 'Главная страница',
        'total_students': total_students,
        'total_courses': total_courses,
        'total_instructors': total_instructors,
        'recent_courses': recent_courses
    })

def student_list(request):
    students = Student.objects.all().order_by('last_name', 'first_name')
    return render(request, 'fefu_lab/student_list.html', {
        'students': students,
        'title': 'Список студентов'
    })

def student_detail(request, pk):
    try:
        student = get_object_or_404(Student, pk=pk)
        enrollments = Enrollment.objects.filter(student=student).select_related('course')
        
        return render(request, 'fefu_lab/student_detail.html', {
            'student': student,
            'enrollments': enrollments,
            'title': f'Студент: {student.first_name} {student.last_name}'
        })
    except Exception as e:
        print(f"Ошибка в student_detail: {e}")
        # В случае ошибки редирект на список студентов
        return redirect('student_list')
def course_list(request):
    courses = Course.objects.filter(is_active=True).select_related('instructor')
    return render(request, 'fefu_lab/course_list.html', {
        'courses': courses,
        'title': 'Список курсов'
    })

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)
    enrollments = Enrollment.objects.filter(course=course, status='ACTIVE').select_related('student')
    
    return render(request, 'fefu_lab/course_detail.html', {
        'course': course,
        'enrollments': enrollments,
        'title': f'Курс: {course.title}'
    })

def enrollment_view(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            try:
                enrollment = form.save(commit=False)
                enrollment.status = 'ACTIVE'
                enrollment.save()
                return redirect('enrollment_success')
            except IntegrityError:
                form.add_error(None, 'Этот студент уже записан на данный курс')
    else:
        form = EnrollmentForm()
    
    return render(request, 'fefu_lab/enrollment.html', {
        'form': form,
        'title': 'Запись на курс'
    })

def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                student = form.save()
                # ВРЕМЕННО: редирект на список студентов вместо деталей
                return redirect('student_list')
                # ИЛИ на главную страницу:
                # return redirect('home')
            except IntegrityError:
                form.add_error('email', 'Студент с таким email уже существует')
            except Exception as e:
                print(f"Ошибка при регистрации: {e}")
                form.add_error(None, f'Произошла ошибка: {e}')
    else:
        form = StudentForm()
    
    return render(request, 'fefu_lab/register.html', {
        'form': form,
        'title': 'Регистрация студента'
    })
def enrollment_success(request):
    return render(request, 'fefu_lab/enrollment_success.html', {
        'title': 'Запись успешно создана'
    })

def feedback_view(request):
    return render(request, 'fefu_lab/feedback.html', {
        'title': 'Обратная связь'
    })
