from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from techinstitute.utils import *

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})  # Make sure Enrollment is imported


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    is_enrolled = False

    if request.user.is_authenticated:
        is_enrolled = course.students.filter(id=request.user.id).exists()

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    # Redirect to payment form where they confirm and initiate payment
    return render(request, 'courses/enroll.html', {'course': course})


def upload_material(request, slug):
    course = get_object_or_404(Course, slug=slug)

    if request.method == 'POST' and request.FILES.get('file'):
        material = CourseMaterial.objects.create(
            course=course,
            title=request.POST.get('title'),
            file=request.FILES['file']
        )
        material_url = request.build_absolute_uri(material.get_absolute_url())
        notify_new_material(course, material_url)
        return redirect('course_detail', slug=slug)

    return render(request, 'courses/upload_material.html', {'course': course})

