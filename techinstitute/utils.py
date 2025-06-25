# techinstitute/utils.py

from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Notification, Payment


def notify_new_material(course, material_url):
    """Notify all verified users of a specific course about a new material"""
    paid_users = Payment.objects.filter(course=course, verified=True).values_list('user', flat=True).distinct()

    for user_id in paid_users:
        user = User.objects.get(id=user_id)
        
        Notification.objects.create(
            user=user,
            title="New Material Added",
            message=f"New material has been added to {course.title}.",
            url=material_url
        )

        send_email_notification(
            user,
            subject="New Course Material Available",
            message=f"Hello {user.get_full_name() or user.username},\n\nNew material has been added to {course.title}. Check it out here: {material_url}"
        )


def send_meet_notification(course, meet_url):
    """Notify all verified users of a specific course about a Google Meet class"""
    paid_users = Payment.objects.filter(course=course, verified=True).values_list('user', flat=True).distinct()

    for user_id in paid_users:
        user = User.objects.get(id=user_id)
        
        Notification.objects.create(
            user=user,
            title="Google Meet Class Scheduled",
            message="Join the class at 4 PM. Click below for instructions.",
            url=meet_url
        )

        send_email_notification(
            user,
            subject="Live Class Scheduled",
            message=f"Dear {user.get_full_name() or user.username},\n\nA live class has been scheduled for {course.title}. Join here: {meet_url}"
        )


def notify_all_paid_users(title, message, url=None):
    """Send a custom notification to all users who paid for any course"""
    paid_user_ids = Payment.objects.filter(verified=True).values_list('user', flat=True).distinct()

    for user_id in paid_user_ids:
        try:
            user = User.objects.get(id=user_id)
            Notification.objects.create(
                user=user,
                title=title,
                message=message,
                url=url or ""
            )
            send_email_notification(
                user,
                subject=title,
                message=message
            )
        except User.DoesNotExist:
            continue


def send_email_notification(user, subject, message):
    if user.email:
        send_mail(
            subject,
            message,
            'edidiongeka54@gmail.com',  # Replace with verified sender email
            [user.email],
            fail_silently=True,
        )


from django.conf import settings
import requests

def generate_groq_response(prompt):
    api_key = settings.GROQ_API_KEY

    if not api_key:
        return "Error: GROQ API key not found."

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Request error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def send_sms(to, message, sender_id="Calisa acad"):
    url = "https://api.ng.termii.com/api/sms/send"
    payload = {
        "to": to,
        "from": sender_id,
        "sms": message,
        "type": "plain",
        "channel": "generic",
        "api_key": settings.TERMII_API_KEY
    }
    response = requests.post(url, json=payload)
    return response.json()