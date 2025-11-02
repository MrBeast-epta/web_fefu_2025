from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View
# FBV для главной страницы
def home_page(request):
    return render(request, 'fefu_lab/home.html')
# FBV для страницы "О нас"
def about_page(request):
    return render(request, 'fefu_lab/about.html')
# CBV для профиля студента (динамический маршрут)
class StudentProfileView(View):
    def get(self, request, student_id):
        if student_id > 100:
            raise Http404("Студент не найден")
        context = {'student_id': student_id}
        return render(request, 'fefu_lab/student_profile.html', context)
# FBV для деталей курса (динамический маршрут)
def course_detail(request, course_slug):
    valid_slugs = ['python', 'django']
    if course_slug not in valid_slugs:
        raise Http404("Курс не найден")
    context = {'course_slug': course_slug}
    return render(request, 'fefu_lab/course_detail.html', context)

def page_not_found(request, exception):
    return render(request, 'fefu_lab/404.html', status=404)
