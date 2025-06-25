from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from courses.models import Course
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.urls import reverse
import requests
import uuid


def index(request):
    return render(request, 'techinstitute/home.html')



@csrf_exempt
@login_required
def initialize_payment(request, slug):
    import uuid
    from courses.models import Course
    from django.conf import settings

    reference = str(uuid.uuid4())
    course = get_object_or_404(Course, slug=slug)

    if request.method == 'POST':
        user = request.user

        name = user.get_full_name() or user.username
        email = user.email

        if not email:
            return JsonResponse({'error': 'Your account does not have a valid email address'}, status=400)

        amount = int(course.price * 100)  # in kobo

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        callback_url = request.build_absolute_uri(
            reverse('verify-payment') + f'?reference={reference}'
        )

        data = {
            'email': email,
            'amount': amount,
            'reference': reference,
            'metadata': {
                'name': name,
                'user_id': user.id,
                'course_slug': course.slug,
            },
            'callback_url': callback_url,
        }

        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, json=data)
        response_data = response.json()

        if response_data.get('status') and response_data['data'].get('authorization_url'):
            return redirect(response_data['data']['authorization_url'])
        else:
            return JsonResponse({'error': response_data.get('message', 'Unable to initialize payment')}, status=500)

    return redirect('course_list')

# views.py
@csrf_exempt
def verify_payment(request):
    from courses.models import Course  # cross-app import
    reference = request.GET.get('reference')

    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()

    if response_data['status'] and response_data['data']['status'] == 'success':
        metadata = response_data['data']['metadata']
        user = get_object_or_404(User, id=metadata['user_id'])
        course = get_object_or_404(Course, slug=metadata['course_slug'])

        # Enroll user in course
        course.students.add(user)

        # Optionally save to a Payment model if you have one
        Payment.objects.create(
            user=user,
            course=course,
            amount=course.price,
            payment_reference=reference,
            verified=True
        )

        messages.success(request, f"You are now enrolled in {course.title}")
        return redirect('dashboard')  # or 'course_detail' with course.slug
    else:
        messages.error(request, 'Payment verification failed.')
        return redirect('course_list')
    

# app_name/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Notification


# techinstitute/views.py
@login_required
def notifications_view(request):
    user_notifications = request.user.notifications.all().order_by('-created_at')
    # Mark all as read
    user_notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'techinstitute/notifications.html', {
        'user_notifications': user_notifications
    })



# techinstitute/views.py
from .utils import send_meet_notification

@login_required
def upload_class_link(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)

    if request.method == 'POST':
        meet_url = request.POST.get('meet_url')

        # TODO: Save class link to a model or wherever needed

        # Trigger notifications
        send_meet_notification(course, meet_url)

        messages.success(request, "Meet link uploaded and notifications sent.")
        return redirect('dashboard')

    return render(request, 'techinstitute/upload_link.html', {'course': course})



from django.shortcuts import render
from .utils import generate_groq_response

def ai_chat_view(request):
    reply = ""
    if request.method == "POST":
        user_prompt = request.POST.get("prompt")
        if user_prompt:
            reply = generate_groq_response(user_prompt)
    return render(request, "techinstitute/chat.html", {"reply": reply})


from django.http import JsonResponse
from .utils import send_sms

def test_sms_view(request):
    to = "+2349137531738"  # Nigerian number in international format
    message = "Hello from Termii API Test!"
    response = send_sms(to, message)
    return JsonResponse(response) 
